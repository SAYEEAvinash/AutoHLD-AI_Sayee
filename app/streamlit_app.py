import sys, tempfile
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from app.services.document_processor import load_document, chunk_pages
from app.services.retriever import build_retriever
from app.services.extractor import extract_entities, extract_relationships, detect_issues
from app.services.llm import ollama_answer, extractive_answer
from app.services.report import build_report

st.set_page_config(page_title="AutoHLD-AI", page_icon="🚗", layout="wide")
st.title("🚗 AutoHLD-AI")
st.caption("AI-Powered AUTOSAR HLD Analysis and Architecture Traceability Assistant")

with st.sidebar:
    st.header("Workspace")
    prefer_embeddings = st.checkbox("Use local sentence-transformer embeddings", value=True)
    use_llm = st.checkbox("Use local Ollama LLM", value=True)
    top_k = st.slider("Evidence chunks", 2, 8, 5)
    st.warning("Synthetic demo data is for academic evaluation only. AI outputs require human review.")

uploaded = st.file_uploader("Upload an HLD document", type=["pdf", "txt", "md"])

if not uploaded:
    st.info("Upload data/hld_corpus/HLD_01_vehicle_control.txt to run the complete demo.")
    st.markdown("""
### Recommended demo sequence
1. Upload `HLD_01_vehicle_control.txt`.
2. Ask: **Which components communicate with DiagnosticManager?**
3. Open **Architecture Graph**.
4. Open **Issues & Traceability**.
5. Download the generated report.
""")
    st.stop()

with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
    tmp.write(uploaded.getvalue())
    path = tmp.name

pages = load_document(path)
chunks = chunk_pages(pages)
retriever = build_retriever(chunks, prefer_embeddings=prefer_embeddings)
entities = extract_entities(chunks)
relationships = extract_relationships(chunks)
issues = detect_issues(chunks, entities, relationships)

a,b,c,d,e = st.columns(5)
a.metric("Pages", len(pages))
b.metric("Chunks", len(chunks))
c.metric("Entities", len(entities))
d.metric("Relations", len(relationships))
e.metric("Issues", len(issues))

tabs = st.tabs(["💬 Q&A", "🧩 Architecture Graph", "⚠️ Issues & Traceability", "📄 Report"])

with tabs[0]:
    st.subheader("Evidence-grounded engineering Q&A")
    question = st.text_input("Architecture question", placeholder="Which components communicate with DiagnosticManager?")
    if question:
        evidence = retriever.search(question, top_k)
        answer = ollama_answer(question, evidence) if use_llm else None
        st.markdown(answer or extractive_answer(question, evidence))
        st.divider()
        st.subheader("Retrieved evidence")
        for ch, score in evidence:
            st.markdown(f"**Page {ch.page} · score {score:.3f}**")
            st.write(ch.text)

with tabs[1]:
    st.subheader("Architecture entity inventory")
    if entities:
        st.dataframe(pd.DataFrame([e.__dict__ for e in entities])[["entity_type","name","page"]],
                     use_container_width=True, hide_index=True)
    G = nx.DiGraph()
    for r in relationships:
        G.add_edge(r.source, r.target, relation=r.relation, page=r.page)
    if G.number_of_edges():
        pos = nx.spring_layout(G, seed=42)
        ex, ey = [], []
        for u,v in G.edges():
            ex += [pos[u][0], pos[v][0], None]
            ey += [pos[u][1], pos[v][1], None]
        edge = go.Scatter(x=ex, y=ey, mode="lines", hoverinfo="none")
        nx_, ny_ = zip(*[pos[n] for n in G.nodes()])
        node = go.Scatter(x=nx_, y=ny_, mode="markers+text",
                          text=list(G.nodes()), textposition="top center",
                          marker={"size":18})
        fig = go.Figure([edge,node])
        fig.update_layout(height=580, margin=dict(l=10,r=10,t=20,b=10),
                          xaxis=dict(showgrid=False,showticklabels=False,zeroline=False),
                          yaxis=dict(showgrid=False,showticklabels=False,zeroline=False))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No explicit relationships detected.")

with tabs[2]:
    st.subheader("Potential issues")
    if issues:
        st.dataframe(pd.DataFrame(issues), use_container_width=True, hide_index=True)
    else:
        st.success("No rule-based issues detected.")
    st.subheader("Traceability coverage")
    st.write("Every generated finding should be reviewed against the source page before engineering use.")

with tabs[3]:
    report = build_report(uploaded.name, entities, relationships, issues)
    st.download_button("Download Markdown report", report, "AutoHLD-AI_Report.md", "text/markdown")
    st.markdown(report)
