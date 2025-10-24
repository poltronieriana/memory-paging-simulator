import sys
import os
import unittest

# Adiciona o diretório raiz do projeto ao PYTHONPATH para permitir importações relativas dos módulos de 'src'.
current_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_dir)

from src.memory import PageTable, PhysicalMemory, TableEntry

class TestMemoryStructures(unittest.TestCase):
    """
    Conjunto de testes unitários para validar as classes
    PageTable, PhysicalMemory e TableEntry (Módulo memory.py).
    """

    def setUp(self):
        """
        Configuração executada antes de cada método de teste.
        Define parâmetros padrão para os testes.
        """
        self.num_pages = 16
        self.num_frames = 8
        self.pt = PageTable(self.num_pages)
        self.pm = PhysicalMemory(self.num_frames)

    def test_01_page_table_creation(self):
        """
        Verifica se a PageTable é instanciada com os valores padrão corretos
        (tamanho correto, entradas não presentes, molduras -1).
        """
        # Verifica o número total de entradas (páginas)
        self.assertEqual(len(self.pt.entries), self.num_pages)
        
        # Verifica se o tipo da entrada é o esperado
        self.assertIsInstance(self.pt.get_entry(0), TableEntry)
        
        # Verifica se uma página arbitrária inicia como 'não presente'
        self.assertFalse(self.pt.is_present(3))
        
        # Verifica se uma página arbitrária inicia sem moldura associada
        self.assertEqual(self.pt.get_frame(5), -1)

    def test_02_physical_memory_creation(self):
        """
        Verifica se a PhysicalMemory é instanciada com os valores padrão corretos
        (número de molduras correto, todas as molduras vazias).
        """
        # Verifica o número total de molduras
        self.assertEqual(self.pm.num_frames, self.num_frames)
        self.assertEqual(len(self.pm.frames), self.num_frames)
        
        # Verifica se uma moldura arbitrária inicia vazia (valor -1)
        self.assertEqual(self.pm.get_page_in_frame(2), -1)

    def test_03_basic_mapping_integration(self):
        """
        Testa a operação de mapeamento (set_mapping) e alocação (allocate_frame)
        de forma integrada, verificando a consistência entre PageTable e PhysicalMemory.
        """
        page_to_load = 5
        frame_to_use = 2
        
        # 1. Mapeia a página 5 para a moldura 2 na Tabela de Páginas
        self.pt.set_mapping(page_to_load, frame_to_use)
        
        # 2. Aloca a página 5 na moldura 2 da Memória Física
        self.pm.allocate_frame(frame_to_use, page_to_load)
        
        # 3. Valida se a PageTable reflete o mapeamento
        self.assertTrue(self.pt.is_present(page_to_load))
        self.assertEqual(self.pt.get_frame(page_to_load), frame_to_use)
        
        # 4. Valida se a PhysicalMemory reflete a alocação
        self.assertEqual(self.pm.get_page_in_frame(frame_to_use), page_to_load)

    def test_04_remove_mapping_integration(self):
        """
        Testa a operação de remoção de mapeamento (remove_mapping) e
        liberação de moldura (free_frame) de forma integrada.
        """
        page_to_remove = 7
        frame_to_free = 3
        
        # Estado inicial: Carrega a Página 7 na Moldura 3
        self.pt.set_mapping(page_to_remove, frame_to_free)
        self.pm.allocate_frame(frame_to_free, page_to_remove)
        
        # Verificação pré-remoção
        self.assertTrue(self.pt.is_present(page_to_remove))
        self.assertEqual(self.pm.get_page_in_frame(frame_to_free), page_to_remove)
        
        # 1. Remove o mapeamento da Página 7 na Tabela de Páginas
        self.pt.remove_mapping(page_to_remove)
        
        # 2. Libera a Moldura 3 na Memória Física
        self.pm.free_frame(frame_to_free)
        
        # 3. Valida se a PageTable reflete a remoção
        self.assertFalse(self.pt.is_present(page_to_remove))
        self.assertEqual(self.pt.get_frame(page_to_remove), -1)
        
        # 4. Valida se a PhysicalMemory reflete a liberação
        self.assertEqual(self.pm.get_page_in_frame(frame_to_free), -1)


if __name__ == '__main__':
    unittest.main(verbosity=2)