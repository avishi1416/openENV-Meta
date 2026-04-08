import gradio as gr
from environment import LoanApprovalEnv

def create_app():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="blue")) as demo:
        gr.Markdown("# 🏦 AI Loan Approval & Risk Optimization")
        gr.Markdown("Evaluate applicant baseline data and make strict banking decisions. Maximize rewards by balancing risk safety, fraud prevention, and potential profit.")
        
        env_state = gr.State(LoanApprovalEnv(task_level="hard"))
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📊 Applicant Details")
                with gr.Group():
                    income_ui = gr.Number(label="Income ($)", interactive=False)
                    credit_ui = gr.Number(label="Credit Score", interactive=False)
                    loan_ui = gr.Number(label="Loan Amount ($)", interactive=False)
                    emp_ui = gr.Number(label="Employment Duration (Years)", interactive=False)
                
            with gr.Column():
                gr.Markdown("### ⚖️ AI Decision Engine")
                with gr.Row():
                    approve_btn = gr.Button("✅ Approve Loan", variant="primary")
                    reject_btn = gr.Button("❌ Reject Loan", variant="stop")
                    review_btn = gr.Button("🔍 Flag for Review", variant="secondary")
                
                gr.Markdown("### 🏆 Environment Feedback")
                with gr.Group():
                    status_output = gr.Textbox(label="Last Action Feedback", interactive=False)
                    reward_output = gr.Textbox(label="Reward Earned (0.0 to 1.0)", interactive=False)

        def load_state(env):
            state = env.state()
            return state["income"], state["credit_score"], state["loan_amount"], state["employment_years"], "Ready for evaluation", "Waiting for input..."
            
        def take_action(action, env):
            _, reward, _ = env.step(action)
            # Environment auto-resets on step, mapping to the next applicant
            next_state = env.state()
            msg = f"Applicant {action.upper()}ED! Evaluator awarded: {reward:.2f}"
            return next_state["income"], next_state["credit_score"], next_state["loan_amount"], next_state["employment_years"], msg, str(reward), env

        # Initial load bindings
        demo.load(load_state, inputs=[env_state], outputs=[income_ui, credit_ui, loan_ui, emp_ui, status_output, reward_output])
        
        # Action button bindings
        approve_btn.click(lambda e: take_action("approve", e), inputs=[env_state], outputs=[income_ui, credit_ui, loan_ui, emp_ui, status_output, reward_output, env_state])
        reject_btn.click(lambda e: take_action("reject", e), inputs=[env_state], outputs=[income_ui, credit_ui, loan_ui, emp_ui, status_output, reward_output, env_state])
        review_btn.click(lambda e: take_action("review", e), inputs=[env_state], outputs=[income_ui, credit_ui, loan_ui, emp_ui, status_output, reward_output, env_state])
        
    return demo

app = create_app()

if __name__ == "__main__":
    app.launch()
