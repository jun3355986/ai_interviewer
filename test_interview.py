"""
简单的面试测试脚本 - 演示如何通过API与AI面试官交互
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_interview_flow():
    """测试完整的面试流程"""
    
    print("=" * 50)
    print("AI 面试助手 - 测试流程")
    print("=" * 50)
    
    # 步骤 1: 上传简历（模拟）
    print("\n[步骤 1] 开始面试...")
    resume_content = """
    姓名：张三
    工作经验：5年Java开发经验
    
    项目经验：
    1. 电商系统（2020-2022）
       - 负责订单模块开发，使用Spring Boot + Redis
       - 优化了订单查询性能，响应时间从500ms降低到50ms
       - 使用消息队列处理高并发订单
    
    2. 支付系统（2022-2024）
       - 负责支付网关开发
       - 使用Spring Cloud微服务架构
       - 处理日交易量100万+的支付请求
    """
    
    job_requirements = "Java高级开发工程师，要求3年以上经验，熟悉Spring Boot、Redis、消息队列等"
    
    start_response = requests.post(
        f"{BASE_URL}/interview/start",
        json={
            "resume_content": resume_content,
            "job_requirements": job_requirements,
            "candidate_name": "张三"
        }
    )
    
    if start_response.status_code != 200:
        print(f"❌ 启动面试失败: {start_response.text}")
        return
    
    session_data = start_response.json()
    session_id = session_data["session_id"]
    opening = session_data["opening"]
    
    print(f"✅ 面试已开始，会话ID: {session_id}")
    print(f"\n面试官开场白：\n{opening}\n")
    
    # 步骤 2: 进入自我介绍环节
    print("[步骤 2] 进入自我介绍环节...")
    intro_response = requests.post(f"{BASE_URL}/interview/{session_id}/opening-response")
    intro_data = intro_response.json()
    print(f"\n面试官：{intro_data['question']}\n")
    
    # 模拟自我介绍
    self_intro = "您好，我是张三，有5年Java开发经验，主要从事电商和支付系统的开发工作。"
    print(f"面试者：{self_intro}\n")
    
    intro_answer_response = requests.post(
        f"{BASE_URL}/interview/{session_id}/self-introduction",
        json={
            "session_id": session_id,
            "answer": self_intro
        }
    )
    intro_answer_data = intro_answer_response.json()
    print(f"✅ 面试官：{intro_answer_data['question']}\n")
    
    # 步骤 3: 回答项目问题（模拟几次）
    print("[步骤 3] 项目提问环节...")
    current_question = intro_answer_data['question']
    
    for i in range(2):  # 模拟回答2个问题
        print(f"\n问题 {i+1}: {current_question}")
        
        # 模拟回答
        answer = input("请输入你的回答（或输入 'skip' 跳过）: ").strip()
        if answer.lower() == 'skip':
            answer = "我在这个项目中主要负责订单模块的开发工作，使用了Spring Boot框架和Redis缓存。"
        
        answer_response = requests.post(
            f"{BASE_URL}/interview/{session_id}/project-answer",
            json={
                "session_id": session_id,
                "answer": answer
            }
        )
        
        answer_data = answer_response.json()
        
        if 'score' in answer_data:
            print(f"\n✅ 评分: {answer_data['score']}/100")
            print(f"反馈: {answer_data['feedback']}\n")
        
        if answer_data.get('stage') == 'technical_qna':
            print("📝 项目提问环节结束，进入技术面试环节")
            break
        
        current_question = answer_data.get('question')
        if not current_question:
            break
    
    # 步骤 4: 技术面试（如果需要继续）
    if answer_data.get('stage') == 'technical_qna':
        print("\n[步骤 4] 技术面试环节...")
        tech_start_response = requests.post(
            f"{BASE_URL}/interview/{session_id}/start-technical",
            json={
                "session_id": session_id,
                "question_types": ["Java基础", "多线程", "Spring"],
                "counts": {"Java基础": 2, "多线程": 1, "Spring": 1}
            }
        )
        
        if tech_start_response.status_code == 200:
            tech_data = tech_start_response.json()
            print(f"\n面试官：{tech_data['question']}\n")
            
            # 可以继续回答技术问题...
    
    # 步骤 5: 面试总结
    print("\n[步骤 5] 面试总结...")
    conclude_response = requests.post(f"{BASE_URL}/interview/{session_id}/conclude")
    
    if conclude_response.status_code == 200:
        conclude_data = conclude_response.json()
        print("\n" + "=" * 50)
        print("面试总结")
        print("=" * 50)
        print(f"最终评分: {conclude_data['final_score']}/100")
        if 'average_score' in conclude_data:
            print(f"平均分: {conclude_data['average_score']:.1f}/100")
        print(f"\n反馈:\n{conclude_data['final_feedback']}")
        print("=" * 50)


def test_import_questions():
    """测试导入面试题"""
    print("\n" + "=" * 50)
    print("导入面试题测试")
    print("=" * 50)
    print("\n注意：需要先准备一个面试题PDF或文本文件")
    print("然后通过以下方式导入：")
    print(f"  curl -X POST '{BASE_URL}/interview/questions/import' \\")
    print("    -F 'file=@your_questions.pdf'")
    print("\n或者在浏览器访问 /docs 页面，使用界面导入")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        test_import_questions()
    else:
        test_interview_flow()

