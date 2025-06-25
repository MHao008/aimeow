# multi_tool_agent_langgraph.py
from langchain_openai import ChatOpenAI
from tools_utils import GraphState, read_user_list, extract_ages, write_ages, plot_ages
from langgraph.graph import StateGraph, END

# 初始化 LLM（请替换成你的 key）
llm = ChatOpenAI(temperature=0, model="gpt-4.1", api_key="sk-xxxx", base_url="https://apikfm.com/v1")



# 构建 LangGraph 状态图
workflow = StateGraph(GraphState)
workflow.add_node("read_json", read_user_list)
workflow.add_node("extract_ages", extract_ages)
workflow.add_node("write_ages", write_ages)
workflow.add_node("plot_ages", plot_ages)

# 设置有向流程图
workflow.set_entry_point("read_json") # 设置入口节点
workflow.add_edge("read_json", "extract_ages") # 设置边
workflow.add_edge("extract_ages", "write_ages")
workflow.add_edge("write_ages", "plot_ages")
workflow.add_edge("plot_ages", END) # 设置结束节点

# 构建执行器
app = workflow.compile()

result = app.invoke({
        "input_path": "users.json",
        "ages_output_path": "ages.json"
    })
print("最终输出结果：", result)