import unittest
from repository import Repository


class TestRepository(unittest.TestCase):
    def setUp(self):
        # Cada test usa su propia DB en memoria
        self.repo = Repository(db_path=":memory:")

    # -----------------------------
    # TEST CREACIÓN DE BASE DE DATOS
    # -----------------------------
    def test_base_de_datos_se_crea(self):
        # Al usar :memory:, si se conecta y crea tablas, funciona
        self.assertIsNotNone(self.repo.listar_camiones())
        self.assertIsNotNone(self.repo.listar_camiones_ref())

    # -----------------------------
    # TEST ENTRADA
    # -----------------------------
    def test_registrar_entrada_crea_registro(self):
        matricula = "1497FXP"
        empresa = "Transportes Lorenzo"
        self.repo.registrar_entrada(matricula, empresa)

        registros = self.repo.listar_camiones()
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["matricula"], matricula)
        self.assertEqual(registros[0]["empresa"], empresa)
        self.assertEqual(registros[0]["estado"], "Dentro")

    # -----------------------------
    # TEST SALIDA
    # -----------------------------
    def test_registrar_salida_actualiza_registro(self):
        matricula = "1497FXP"
        empresa = "Transportes Lorenzo"

        self.repo.registrar_entrada(matricula, empresa)
        registro = self.repo.listar_camiones()[0]
        registro_id = registro["id"]

        self.repo.registrar_salida(registro_id)
        registro_actualizado = self.repo.listar_camiones()[0]
        self.assertIsNotNone(registro_actualizado["salida"])
        self.assertEqual(registro_actualizado["estado"], "Fuera")

    # -----------------------------
    # TEST AUTOCOMPLETAR EMPRESA
    # -----------------------------
    def test_autocompletar_empresa_por_matricula(self):
        matricula = "1497FXP"
        empresa = "Transportes Lorenzo"

        self.repo.add_or_update_camion_ref(matricula, empresa)
        resultado = self.repo.get_empresa_by_matricula(matricula)
        self.assertEqual(resultado, empresa)

    # -----------------------------
    # TEST REGISTRO ACTIVO
    # -----------------------------
    def test_get_registro_activo_por_matricula(self):
        matricula = "1497FXP"
        empresa = "Transportes Lorenzo"

        # Entrada
        self.repo.registrar_entrada(matricula, empresa)
        activo = self.repo.get_registro_activo_por_matricula(matricula)
        self.assertIsNotNone(activo)
        self.assertEqual(activo["matricula"], matricula)
        self.assertEqual(activo["estado"], "Dentro")

        # Salida
        self.repo.registrar_salida(activo["id"])
        activo_post_salida = self.repo.get_registro_activo_por_matricula(matricula)
        self.assertIsNone(activo_post_salida)


if __name__ == "__main__":
    unittest.main()
