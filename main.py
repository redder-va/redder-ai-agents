import os
os.chdir(os.path.dirname(__file__))

# Load environment variables before importing modules that use them
from dotenv import load_dotenv
load_dotenv()

# Manual fallback: read .env if load_dotenv didn't set OPENAI_API_KEY
if not os.getenv('OPENAI_API_KEY'):
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    os.environ['OPENAI_API_KEY'] = line.split('=', 1)[1].strip()
                    break
    except FileNotFoundError:
        pass

# Allow pydantic untyped fields for compatibility
os.environ['PYDANTIC_ALLOW_UNTYPED_FIELDS'] = '1'
import pydantic.v1 as pydantic_v1
pydantic_v1.allow_untyped_fields = True

from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.customer_service import CustomerServiceAgent
from agents.content_creator import ContentCreatorAgent
from agents.sales_analyst import SalesAnalystAgent
from agents.marketing import MarketingAgent
from agents.inventory_manager import InventoryManagerAgent
from agents.email_marketing import EmailMarketingAgent
from agents.social_media import SocialMediaAgent
from agents.review_manager import ReviewManagerAgent
from agents.order_manager import OrderManagerAgent
from agents.shipping_manager import ShippingManagerAgent
from agents.loyalty_manager import LoyaltyManagerAgent
from agents.upsell_manager import UpsellManagerAgent
from agents.live_chat import LiveChatAgent
from feedback.feedback_handler import FeedbackHandler
from notifications.whatsapp_notifier import get_whatsapp_notifier
from agents.llm_helper import generate_text

# Production configuration
app = Flask(__name__)

# Load config based on environment
env = os.environ.get('ENVIRONMENT', 'development')
if env == 'production':
    from config import ProductionConfig
    app.config.from_object(ProductionConfig)
    
    # Production CORS - strict
    CORS(app, origins=[
        'https://redder.ro',
        'https://www.redder.ro'
    ])
else:
    # Development CORS - permissive
    CORS(app)

# Rate limiting pentru production
if app.config.get('RATELIMIT_ENABLED'):
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
    )
else:
    limiter = None

# Root health/status route
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "status": "ok",
        "app": "Redder.ro AI Agents",
        "endpoints": [
            "/chat/customer_service",
            "/generate/recipe",
            "/generate/description",
            "/analyze/sales",
            "/predict/sales",
            "/create/campaign",
            "/personalize/recommendation",
            "/check/stock",
            "/suggest/order",
            "/feedback",
            "/feedback/<agent_name>",
            "/workflow/automate_business"
        ]
    })

# Heroku health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "app": "Redder AI Backend"}), 200

# Environment status route (for debugging)
@app.route('/env', methods=['GET'])
def env_status():
    return jsonify({
        "GOOGLE_API_KEY_set": bool(os.environ.get('GOOGLE_API_KEY')),
        "OPENAI_API_KEY_set": bool(os.environ.get('OPENAI_API_KEY')),
        "WC_CONSUMER_KEY_set": bool(os.environ.get('WC_CONSUMER_KEY')),
        "WP_USERNAME_set": bool(os.environ.get('WP_USERNAME'))
    })

# Gemini diagnostic route
@app.route('/gemini/test', methods=['POST'])
def gemini_test():
    data = request.json or {}
    prompt = data.get('prompt', 'Spune un salut scurt în română.')
    # Directly use LLM helper; llm=None triggers Gemini/REST fallback
    output = generate_text(None, prompt, model='gemini-2.0-flash')
    return jsonify({"prompt": prompt, "output": output})

# Lazy initialization of agents
_agents = {}
_feedback_handler = None
_live_chat_agent = None

def get_agent(agent_type):
    """Lazy initialization of agents to speed up startup"""
    global _agents
    if agent_type not in _agents:
        if agent_type == 'customer_service':
            _agents[agent_type] = CustomerServiceAgent()
        elif agent_type == 'content_creator':
            _agents[agent_type] = ContentCreatorAgent()
        elif agent_type == 'sales_analyst':
            _agents[agent_type] = SalesAnalystAgent()
        elif agent_type == 'marketing':
            _agents[agent_type] = MarketingAgent()
        elif agent_type == 'inventory':
            _agents[agent_type] = InventoryManagerAgent()
        elif agent_type == 'email_marketing':
            _agents[agent_type] = EmailMarketingAgent()
        elif agent_type == 'social_media':
            _agents[agent_type] = SocialMediaAgent()
        elif agent_type == 'review_manager':
            _agents[agent_type] = ReviewManagerAgent()
        elif agent_type == 'order_manager':
            _agents[agent_type] = OrderManagerAgent()
        elif agent_type == 'shipping':
            _agents[agent_type] = ShippingManagerAgent()
        elif agent_type == 'loyalty':
            _agents[agent_type] = LoyaltyManagerAgent()
        elif agent_type == 'upsell':
            _agents[agent_type] = UpsellManagerAgent()
    return _agents[agent_type]

def get_feedback_handler():
    """Lazy initialization of feedback handler"""
    global _feedback_handler
    if _feedback_handler is None:
        _feedback_handler = FeedbackHandler()
    return _feedback_handler

def get_live_chat_agent():
    """Lazy initialization of live chat agent"""
    global _live_chat_agent
    if _live_chat_agent is None:
        _live_chat_agent = LiveChatAgent()
    return _live_chat_agent

@app.route('/chat/customer_service', methods=['POST'])
def chat_customer_service():
    data = request.json
    response = get_agent('customer_service').respond(data['text'])
    return jsonify({"response": response})

@app.route('/generate/recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get('text') or data.get('ingredients', '')
    recipe = get_agent('content_creator').generate_recipe(ingredients)
    return jsonify({"recipe": recipe})

@app.route('/generate/description', methods=['POST'])
def generate_description():
    data = request.json
    product = data.get('text') or data.get('product', '')
    description = get_agent('content_creator').generate_description(product)
    return jsonify({"description": description})

@app.route('/analyze/sales', methods=['POST'])
def analyze_sales():
    data = request.json
    data_path = data.get('text') or data.get('data_path', None)
    analysis = get_agent('sales_analyst').analyze_sales_data(data_path)
    return jsonify({"analysis": analysis})

@app.route('/predict/sales', methods=['POST'])
def predict_sales():
    data = request.json
    sales_data = data.get('text') or data.get('data', '')
    prediction = get_agent('sales_analyst').predict_sales(sales_data)
    return jsonify({"prediction": prediction})

@app.route('/create/campaign', methods=['POST'])
def create_campaign():
    data = request.json
    theme = data.get('text') or data.get('theme', '')
    campaign = get_agent('marketing').create_campaign(theme)
    return jsonify({"campaign": campaign})

@app.route('/personalize/recommendation', methods=['POST'])
def personalize_recommendation():
    data = request.json
    profile = data.get('text') or data.get('profile', '')
    recommendation = get_agent('marketing').personalize_recommendation(profile)
    return jsonify({"recommendation": recommendation})

@app.route('/check/stock', methods=['POST'])
def check_stock():
    data = request.json
    item = data.get('text') or data.get('item', '')
    stock = get_agent('inventory').check_stock_levels(item)
    return jsonify({"stock": stock})

@app.route('/suggest/order', methods=['POST'])
def suggest_order():
    data = request.json
    item = data.get('text') or data.get('item', '')
    suggestion = get_agent('inventory').suggest_order(item)
    return jsonify({"suggestion": suggestion})

@app.route('/email/campaign', methods=['POST'])
def email_campaign():
    data = request.json
    campaign_type = data.get('text') or data.get('campaign_type', '')
    campaign = get_agent('email_marketing').create_email_campaign(campaign_type)
    return jsonify({"campaign": campaign})

@app.route('/email/newsletter', methods=['POST'])
def email_newsletter():
    data = request.json
    topic = data.get('text') or data.get('topic', '')
    newsletter = get_agent('email_marketing').generate_newsletter(topic)
    return jsonify({"newsletter": newsletter})

@app.route('/social/post', methods=['POST'])
def social_post():
    data = request.json
    topic = data.get('text') or data.get('topic', '')
    post = get_agent('social_media').create_post(topic)
    return jsonify({"post": post})

@app.route('/social/calendar', methods=['POST'])
def social_calendar():
    data = request.json
    period = data.get('text') or data.get('period', '')
    calendar = get_agent('social_media').generate_content_calendar(period)
    return jsonify({"calendar": calendar})

@app.route('/review/respond', methods=['POST'])
def review_respond():
    data = request.json
    review = data.get('text') or data.get('review', '')
    response = get_agent('review_manager').respond_to_review(review)
    return jsonify({"response": response})

@app.route('/review/analyze', methods=['POST'])
def review_analyze():
    data = request.json
    reviews = data.get('text') or data.get('reviews', '')
    analysis = get_agent('review_manager').analyze_sentiment(reviews)
    return jsonify({"analysis": analysis})

@app.route('/order/process', methods=['POST'])
def order_process():
    data = request.json
    order_details = data.get('text') or data.get('order', '')
    result = get_agent('order_manager').process_order(order_details)
    return jsonify({"result": result})

@app.route('/order/new', methods=['POST'])
def order_new():
    """
    Endpoint pentru procesarea comenzilor noi cu notificare WhatsApp automată
    
    Exemplu payload:
    {
        "order_number": "12345",
        "customer_name": "Ion Popescu",
        "customer_phone": "0721123456",
        "customer_email": "ion@email.com",
        "items": [
            {"name": "Vodca Kumaniok Original 38%", "quantity": 2, "price": 24.00},
            {"name": "ORO del Sole Peach", "quantity": 1, "price": 24.00}
        ],
        "total": 72.00,
        "payment_method": "Ramburs",
        "shipping_address": "Str.Example 123, București, Sector 1",
        "notes": "Livrare între 14-16"
    }
    """
    data = request.json
    
    # Trimite notificare WhatsApp
    whatsapp = get_whatsapp_notifier()
    notification_sent = whatsapp.send_order_notification(data)
    
    # Procesează comanda și cu agentul (pentru context și învățare)
    order_text = f"Comandă nouă #{data.get('order_number')} de la {data.get('customer_name')}"
    agent_result = get_agent('order_manager').process_order(order_text)
    
    return jsonify({
        "status": "success",
        "order_number": data.get('order_number'),
        "whatsapp_notification_sent": notification_sent,
        "agent_response": agent_result
    })

@app.route('/order/track', methods=['POST'])
def order_track():
    data = request.json
    order_id = data.get('text') or data.get('order_id', '')
    tracking = get_agent('order_manager').track_order(order_id)
    return jsonify({"tracking": tracking})

@app.route('/shipping/calculate', methods=['POST'])
def shipping_calculate():
    data = request.json
    details = data.get('text') or data.get('details', '')
    shipping = get_agent('shipping').calculate_shipping(details)
    return jsonify({"shipping": shipping})

@app.route('/shipping/track', methods=['POST'])
def shipping_track():
    data = request.json
    awb = data.get('text') or data.get('awb', '')
    tracking = get_agent('shipping').track_delivery(awb)
    return jsonify({"tracking": tracking})

@app.route('/loyalty/points', methods=['POST'])
def loyalty_points():
    data = request.json
    activity = data.get('text') or data.get('activity', '')
    points = get_agent('loyalty').calculate_points(activity)
    return jsonify({"points": points})

@app.route('/loyalty/program', methods=['POST'])
def loyalty_program():
    data = request.json
    segment = data.get('text') or data.get('segment', '')
    program = get_agent('loyalty').create_vip_program(segment)
    return jsonify({"program": program})

@app.route('/upsell/suggest', methods=['POST'])
def upsell_suggest():
    data = request.json
    cart = data.get('text') or data.get('cart', '')
    suggestions = get_agent('upsell').suggest_upsell(cart)
    return jsonify({"suggestions": suggestions})

@app.route('/crosssell/suggest', methods=['POST'])
def crosssell_suggest():
    data = request.json
    cart = data.get('text') or data.get('cart', '')
    suggestions = get_agent('upsell').suggest_crosssell(cart)
    return jsonify({"suggestions": suggestions})

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    get_feedback_handler().store_feedback(data['agent_name'], data['feedback'], data['rating'])
    return jsonify({"status": "Feedback stored"})

@app.route('/feedback/<agent_name>', methods=['GET'])
def get_feedback(agent_name):
    feedbacks = get_feedback_handler().get_feedback(agent_name)
    return jsonify({"feedbacks": feedbacks})

# Workflow example
@app.route('/workflow/automate_business', methods=['POST'])
def automate_business():
    # Simple workflow: simulate
    result = "Business automated: Inventory checked, sales analyzed, campaign created."
    return jsonify({"result": result})

# Live Chat Endpoint pentru website
@app.route('/chat/message', methods=['POST'])
def chat_message():
    """Endpoint pentru chat live pe website
    Rate limit: 10 requests/minute per IP (production)
    """
    # Apply rate limiting in production
    if limiter and app.config.get('ENVIRONMENT') == 'production':
        try:
            limiter.limit("10 per minute")(lambda: None)()
        except:
            return jsonify({
                'success': False,
                'error': 'Prea multe cereri. Te rog așteaptă un moment.',
                'response': 'Ai trimis prea multe mesaje. Te rog așteaptă 1 minut. 🙏'
            }), 429
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        session_id = data.get('session_id', '')
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Mesajul nu poate fi gol'
            }), 400
        
        # Logging pentru production
        if app.config.get('ENVIRONMENT') == 'production':
            import logging
            logging.info(f"Chat request - Session: {session_id[:12]}..., Message length: {len(user_message)}")
        
        # Obține agent chat
        chat_agent = get_live_chat_agent()
        
        # Procesează mesajul
        result = chat_agent.chat(user_message, conversation_history)
        
        # Adaugă quick replies
        if result.get('success'):
            result['quick_replies'] = chat_agent.get_quick_replies(result.get('intent', 'general_inquiry'))
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        print(f"\n[EROARE CHAT] {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'Îmi pare rău, am întâmpinat o problemă. Te rog încearcă din nou. 🙏'
        }), 500

if __name__ == "__main__":
    import os
    
    # Heroku folosește variabila PORT
    port = int(os.environ.get('PORT', 5000))
    
    # SSL Configuration pentru HTTPS localhost (doar development)
    ssl_cert = os.path.join(os.path.dirname(__file__), 'ssl', 'localhost.pem')
    ssl_key = os.path.join(os.path.dirname(__file__), 'ssl', 'localhost-key.pem')
    
    # Production (Heroku) - fără SSL (Heroku oferă SSL automat)
    if os.environ.get('FLASK_ENV') == 'production':
        print(f"[PRODUCTION] Starting on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    # Development - cu SSL
    elif os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        print("[HTTPS] Starting with HTTPS on https://127.0.0.1:5000")
        app.run(host='127.0.0.1', port=5000, debug=True, ssl_context=(ssl_cert, ssl_key))
    else:
        print("[HTTP] SSL certificates not found. Starting with HTTP on http://127.0.0.1:5000")
        print(f"    Expected cert: {ssl_cert}")
        print(f"    Run setup_https_auto.ps1 to generate certificates")
        app.run(host='127.0.0.1', port=5000, debug=True)