import sys
from simulator import Simulator
from interface import Interface

def main():
    """
    Ponto de entrada principal da simulação.
    
    Responsável pela integração:
    1. Instancia os componentes (Interface, Simulador).
    2. Coleta as entradas (via Interface).
    3. Conecta a Interface ao Simulador (callbacks).
    4. Inicia a simulação.
    """
    
    # 1. Instancia os componentes
    ui = Interface()
    
    # Verifica se o modo 'demo' foi solicitado
    if "demo" in sys.argv:
        ui.set_demo_mode(True)
    else:
        ui.set_demo_mode(False) # Se não for posto como verdadeiro, irá pergunta ao usuário.

    # 2. Coleta as entradas
    num_frames, num_pages, access_list = ui.get_inputs()
    
    # 3. Instancia o Simulador 
    sim = Simulator(num_frames, num_pages)
    
    # 4. Conecta a Interface ao Simulador 
    # Passa as funções de 'ui' para o simulador usar como callbacks.
    sim.set_display_callbacks(
        display_step=ui.display_step,
        display_report=ui.display_final_report
    )
    
    # 5. Inicia a simulação
    try:
        sim.run(access_list)
    except Exception as e:
        print(f"\nErro crítico durante a simulação: {e}")
        print("Verifique a implementação (provavelmente no simulador ou memória).")

if __name__ == "__main__":
    main()