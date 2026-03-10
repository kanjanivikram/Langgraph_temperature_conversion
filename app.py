from flask import Flask, render_template, request, jsonify
from main import create_web_graph
import os

app = Flask(__name__)

# Create the graph instance
graph_builder = create_web_graph()

@app.route('/')
def home():
    """Render the main temperature converter page"""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """API endpoint to convert temperature"""
    try:
        data = request.json
        temp = float(data['temperature'])
        scale = data['scale'].upper()
        
        # Validate scale
        if scale not in ['C', 'F']:
            return jsonify({
                'success': False,
                'error': 'Invalid scale. Must be C or F'
            }), 400
        
        # Prepare state and run graph
        if scale == 'C':
            state = {'celsius': temp, 'fahrenheit': 0.0, 'conversion_type': 'c_to_f'}
            result = graph_builder.invoke(state)
            message = f"{result['celsius']}°C = {result['fahrenheit']}°F"
        else:
            state = {'celsius': 0.0, 'fahrenheit': temp, 'conversion_type': 'f_to_c'}
            result = graph_builder.invoke(state)
            message = f"{result['fahrenheit']}°F = {result['celsius']}°C"
        
        return jsonify({'success': True, 'result': message})
    
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'temperature-converter'})

if __name__ == '__main__':
    print("Starting Temperature Converter Flask App")
    print("Access the app at: http://localhost:5000")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
