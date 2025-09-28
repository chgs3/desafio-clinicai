import os
from typing import TypedDict, List
from dotenv import load_dotenv
import google.generativeai as genai

# configurando o LLM Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = genai.GenerativeModel('gemini-2.5-flash')
chat_sessions = {}

# definindo o estado da triagem
class TriageState(TypedDict):
    chat_id: str
    historico_chat: List[str]
    queixa_principal: str
    sintomas_detalhados: str
    duracao_frequencia: str
    intensidade: str
    historico_relevante: str
    medidas_tomadas: str
    resumo: str

# avaliando o prompt com o histórico
def create_prompt(base_prompt: str, history: List[str]):
    history_str = "\n".join(history)
    return f"""Você é um assistente de triagem da ClinicAI. Seja empático, profissional e claro.
Histórico da Conversa:
{history_str}

Sua Tarefa Agora: {base_prompt}"""

# função principal do agente
async def run_agent_turn(chat_id: str, user_message: str) -> dict:
    state = chat_sessions.get(chat_id)
    if not state:
        state = TriageState(
            chat_id=chat_id, historico_chat=[], queixa_principal="", sintomas_detalhados="",
            duracao_frequencia="", intensidade="", historico_relevante="", medidas_tomadas="", resumo=""
        )
    
    state['historico_chat'].append(f"Usuário: {user_message}")
    
    agent_response = ""
    is_complete = False # variável pra indicar se a triagem acabou

    # lógica de estado da triagem
    if not state['queixa_principal']:
        state['queixa_principal'] = user_message
        prompt_para_llm = f"Apresente-se calorosamente como o assistente da ClinicAI. Confirme o recebimento da queixa principal ('{user_message}'), explique que você não é um médico e peça ao usuário para descrever os sintomas em detalhes."

    elif not state['sintomas_detalhados']:
        state['sintomas_detalhados'] = user_message
        prompt_para_llm = "Agradeça ao usuário pelas informações. Peça a ele para informar desde quando os sintomas começaram e com que frequência ocorrem."

    elif not state['duracao_frequencia']:
        state['duracao_frequencia'] = user_message
        prompt_para_llm = "Agradeça e peça ao usuário para classificar a intensidade do desconforto em uma escala de 0 a 10, onde 10 é o máximo."

    elif not state['intensidade']:
        state['intensidade'] = user_message
        prompt_para_llm = "Entendido. Pergunte ao usuário se ele tem alguma condição de saúde pré-existente ou histórico de problemas similares."

    elif not state['historico_relevante']:
        state['historico_relevante'] = user_message
        prompt_para_llm = "Obrigado. Para finalizar, pergunte quais medidas ou medicamentos o usuário já tomou para aliviar os sintomas."

    elif not state['medidas_tomadas']:
        state['medidas_tomadas'] = user_message
        is_complete = True # triagem completa
        
        # gerando o resumo final       
        print("Gerando Resumo Final com LLM...")
        
        summary_prompt = f"""Crie um resumo estruturado da triagem:
        - Queixa Principal: {state['queixa_principal']}
        - Sintomas: {state['sintomas_detalhados']}
        - Duração/Frequência: {state['duracao_frequencia']}
        - Intensidade: {state['intensidade']}
        - Histórico: {state['historico_relevante']}
        - Medidas Tomadas: {state['medidas_tomadas']}
        """
        summary_response = llm.generate_content(summary_prompt)
        state['resumo'] = summary_response.text
        print(f"RESUMO GERADO:\n{state['resumo']}")

        agent_response = "Muito obrigado por todas as informações. Seu resumo de triagem foi registrado e nossa equipe entrará em contato em breve. Se cuide!"
        state['historico_chat'].append(f"Agente: {agent_response}")
        chat_sessions[chat_id] = state
        # Retorna um dicionário com as informações completas
        return {"response": agent_response, "is_complete": is_complete, "state": state}
    
    else:
        agent_response = "Sua triagem já foi concluída. Nossa equipe entrará em contato em breve. Para uma nova queixa, por favor, inicie um 'Novo Chat'."
        state['historico_chat'].append(f"Agente: {agent_response}")
        chat_sessions[chat_id] = state
        return {"response": agent_response, "is_complete": True, "state": state}

    # --- CHAMADA PRINCIPAL AO LLM ---
    print(f"Enviando prompt para o LLM: {prompt_para_llm}")
    full_prompt = create_prompt(prompt_para_llm, state['historico_chat'])
    
    response_do_llm = llm.generate_content(full_prompt)
    agent_response = response_do_llm.text

    state['historico_chat'].append(f"Agente: {agent_response}")
    chat_sessions[chat_id] = state
    
    # Retorna um dicionário com as informações completas
    return {"response": agent_response, "is_complete": is_complete, "state": state}