from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('material')
class TestMaterial(TransactionCase):

    def setUp(self):
        super().setUp()
        self.supplier = self.env['res.partner'].create({'name': 'Test Supplier'})

    def test_create_material_success(self):
        """Test creating material successfully"""
        material = self.env['material'].create({
            'material_code': 'MAT001',
            'material_name': 'Blue Fabric',
            'material_type': 'fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id
        })
        self.assertTrue(material.id)

    def test_create_material_fail_price(self):
        """Test creating material with invalid price"""
        with self.assertRaises(ValidationError):
            self.env['material'].create({
                'material_code': 'MAT002',
                'material_name': 'Cheap Fabric',
                'material_type': 'fabric',
                'material_buy_price': 50,
                'supplier_id': self.supplier.id
            })
