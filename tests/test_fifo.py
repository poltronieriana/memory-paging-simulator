import sys
import os
import unittest

# Adiciona o diretório raiz do projeto ao PYTHONPATH
current_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_dir)

from src.simulator import Simulator
from src.interface import Interface

class TestFIFOLogic(unittest.TestCase):
    """
    Testa a lógica de integração e o algoritmo FIFO
    """

    def setUp(self):
        """
        configura um simulador limpo e uma interface mockada
        para silenciar os prints durante os testes.
        """
        self.mock_interface = Interface()
        # Redireciona os callbacks para funções vazias
        self.mock_interface.display_step = lambda state: None 
        self.mock_interface.display_final_report = lambda report: None
        
        # Redireciona o stdout para /dev/null (ou NUL no Windows) para
        # suprimir os prints de "HIT", "FAULT", etc.
        self.dev_null = open(os.devnull, 'w')
        self.original_stdout = sys.stdout
        sys.stdout = self.dev_null

    def tearDown(self):
        """
        Restaura o stdout original após cada teste.
        """
        sys.stdout = self.original_stdout
        self.dev_null.close()

    def test_01_fifo_simulation_3_frames(self):
        """
        Valida o algoritmo FIFO com 3 molduras.
        Sequência: 0 1 2 3 0 1 4
        Resultado Esperado: 7 falhas de página.
        """
        num_frames = 3
        num_pages = 8 # (Qualquer valor >= 5 para este teste)
        access_list = "0 1 2 3 0 1 4".split()
        
        sim = Simulator(num_frames, num_pages)
        
        # Conecta a interface mockada
        sim.set_display_callbacks(
            display_step=self.mock_interface.display_step,
            display_report=self.mock_interface.display_final_report
        )
        
        # Executa a simulação
        sim.run(access_list)
        
        # Validação 
        expected_faults = 7
        self.assertEqual(
            sim.page_faults, 
            expected_faults,
            f"Falha no Teste FIFO (3 Molduras): Esperado {expected_faults} page faults, mas obteve {sim.page_faults}"
        )
        
        # Valida o estado final da memória
        # Fila: [0, 1, 2] -> [1, 2, 3] -> [2, 3, 0] -> [3, 0, 1] -> [0, 1, 4]
        present_pages = sorted([page for page in sim.physical_memory.frames if page != -1])
        expected_pages_in_memory = [0, 1, 4]
        
        self.assertListEqual(
            present_pages, 
            expected_pages_in_memory,
            f"Falha no Teste FIFO (Estado da Memória): Páginas esperadas {expected_pages_in_memory}, mas obteve {present_pages}"
        )

    def test_02_fifo_simulation_page_hits(self):
        """
        Testa uma sequência com Page Hits para garantir que não
        incrementam as falhas.
        Sequência: 1 2 3 1 2 3 4 4
        Resultado Esperado: 4 falhas.
        """
        num_frames = 4
        num_pages = 8
        access_list = "1 2 3 1 2 3 4 4".split()
        
        sim = Simulator(num_frames, num_pages)
        sim.set_display_callbacks(
            display_step=self.mock_interface.display_step,
            display_report=self.mock_interface.display_final_report
        )
        
        sim.run(access_list)
        
        expected_faults = 4 # (1, 2, 3, e 4 são falhas; o resto é hit)
        self.assertEqual(
            sim.page_faults, 
            expected_faults,
            f"Falha no Teste FIFO (Page Hits): Esperado {expected_faults} page faults, mas obteve {sim.page_faults}"
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)