# agente_gerador_post_linkedin.py

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Configuração de ferramentas
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agentes
buscador = Agent(
    role='Buscador de Conteúdo',
    goal='Busque conteúdo online sobre o tema: {tema}.',
    backstory=(
        'Você é responsável por buscar conteúdos relacionados ao tema {tema}. '
        'Encontre informações que conectem com o público corporativo e inovador.'
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)

redator = Agent(
    role='Redator de Conteúdo',
    goal='Crie um texto didático e alinhado ao tema: {tema}.',
    backstory=(
        'Redija um texto assertivo e direto, conectado ao tema {tema}.'
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)

editor = Agent(
    role='Editor de Conteúdo',
    goal='Edite o texto gerado pelo Redator de Conteúdo sobre o tema: {tema}.',
    backstory=(
        'Revise o texto para garantir clareza, impacto e conexão emocional.'
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)

# Tarefas
buscar = Task(
    description="Busque conteúdos relevantes sobre o tema.",
    agent=buscador,
    expected_output="Lista de conteúdos relevantes sobre o tema."
)

redigir = Task(
    description="Escreva um texto alinhado ao tema e ao estilo do usuário.",
    agent=redator,
    expected_output="Texto inicial gerado para o tema."
)

editar = Task(
    description="Edite o texto para garantir consistência e clareza.",
    agent=editor,
    expected_output="Texto final revisado e pronto para publicação."
)

# Equipe
equipe = Crew(
    agents=[buscador, redator, editor],
    tasks=[buscar, redigir, editar],
    verbose=True
)

# Função para gerar posts
def gerar_post(tema):
    entradas = {"tema": tema}
    try:
        resultado = equipe.kickoff(inputs=entradas)
        texto_final = resultado.tasks_output[-1]  # Ajuste conforme o atributo correto
        return texto_final
    except Exception as e:
        return f"Erro ao gerar o texto: {str(e)}"
