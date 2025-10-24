class Interface:
    """
    Responsável por toda a exibição textual (saída) e coleta
    de dados (entrada) da simulação.
    """

    def __init__(self):
        """
        Inicializa a interface.
        """
        self.step_by_step = False

    def set_demo_mode(self, enabled=True):
        """
        Ativa ou desativa o modo de demonstração (passo a passo).
        """
        self.step_by_step = enabled
        if self.step_by_step:
            print("[Interface] Modo demonstração (passo a passo) ativado.")

    def display_step(self, state_data):
        """
        Exibe o estado da simulação após um acesso.
        
        Args:
            state_data (dict): Dicionário vindo de simulator.get_simulation_state()
        """
        
        # TODO: integrante 4 mexe aqui
        
        print(f"[Interface Stub] Exibindo estado. (Lógica de I4 pendente)")
        
        if self.step_by_step:
            input("  Pressione Enter para o próximo acesso...")

    def display_final_report(self, report_data):
        """
        Exibe o relatório final da simulação.

        Args:
            report_data (dict): Dicionário vindo de simulator.get_final_report()
        """
        
        # TODO: integrante 4 mexe aqui 
        
        print("=" * 50)
        print("[Interface Stub] RELATÓRIO FINAL (Lógica de I4 pendente)")
        print(f"Total de Falhas de Página: {report_data['total_page_faults']}")
        print("=" * 50)


    def get_inputs(self):
        """
        Coleta as entradas do usuário (Tamanhos de memória e lista de acessos).
        
        Retorna:
            tuple: (num_frames, num_pages, access_list)
        """
        
        # TODO: integrante 1 mexe aqui
        
        print("[Interface Stub] Usando entradas padrão. (Lógica de I1 pendente)")
        
        # Valores provisórios para permitir a execução 
        num_frames = 4
        num_pages = 8
        access_list = "0 1 2 3 0 1 4 0 1 2 3 4".split()
        
        return num_frames, num_pages, access_list