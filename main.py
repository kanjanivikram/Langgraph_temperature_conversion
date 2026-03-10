from IPython.display import Image, display
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
# from dotenv import load_dotenv

# load_dotenv()

class ConversionState(TypedDict):
    celsius: float
    fahrenheit: float
    conversion_type: str

def input_temperature(state:ConversionState) -> ConversionState:
    choice_type = input('Enter the temperature scale you want to convert C/F: ').upper()

    if choice_type == 'C':
        state['conversion_type'] = 'c_to_f'
        state['celsius'] = float(input('Enter the temperature in Celsius: '))
    elif choice_type == 'F':
        state['conversion_type'] = 'f_to_c'
        state['fahrenheit'] = float(input('Enter the temperature in Fahrenheit: '))

    return state


def celsius_to_fahrenheit(state:ConversionState) -> ConversionState:
    state['fahrenheit'] = (state['celsius'] * 9/5) + 32
    return state

def fahrenheit_to_celsius(state:ConversionState) -> ConversionState:
    state['celsius'] = (state['fahrenheit'] - 32) * 5/9
    return state

def route_conversion(state:ConversionState) -> str:
    return state['conversion_type']


def create_web_graph():
        graph = StateGraph(ConversionState)
        graph.add_node("c_to_f", celsius_to_fahrenheit)
        graph.add_node("f_to_c", fahrenheit_to_celsius)
        graph.add_conditional_edges(START,
                                    route_conversion, 
                                    {'c_to_f':'c_to_f',
                                    'f_to_c':'f_to_c'})
        graph.add_edge("c_to_f", END)
        graph.add_edge("f_to_c", END)

        graph_builder = graph.compile()
        return graph_builder

