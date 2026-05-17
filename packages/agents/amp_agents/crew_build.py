"""CrewAI parallel build agents: SEO, Content, Web."""

from crewai import Agent, Crew, Process, Task


def build_creative_crew(tenant_id: str, brief: str) -> Crew:
    seo = Agent(
        role="SEO Agent",
        goal="Produce JSON-LD schema markup and AEO-optimized metadata",
        backstory="Expert in SXO, GEO, and Google Indexing API cold-start.",
        verbose=False,
    )
    content = Agent(
        role="Content Agent",
        goal="Draft compliant copy with FTC/CMA transparency",
        backstory="Creates channel-ready assets from the strategy brief.",
        verbose=False,
    )
    web = Agent(
        role="Web Agent",
        goal="Assemble landing pages with structured data",
        backstory="Implements frictionless UX per SXO guidelines.",
        verbose=False,
    )

    tasks = [
        Task(
            description=f"[{tenant_id}] SEO: {brief}. Output JSON-LD FAQ schema.",
            agent=seo,
            expected_output="JSON-LD block and meta tags",
        ),
        Task(
            description=f"[{tenant_id}] Content: {brief}",
            agent=content,
            expected_output="Ad copy and email variants",
        ),
        Task(
            description=f"[{tenant_id}] Web: {brief}",
            agent=web,
            expected_output="Landing page HTML outline",
        ),
    ]

    return Crew(agents=[seo, content, web], tasks=tasks, process=Process.parallel)
