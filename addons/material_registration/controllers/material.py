from odoo import http
from odoo.http import request

class MaterialController(http.Controller):

    @http.route('/materials', type='json', auth='public', methods=['GET'])
    def get_materials(self, material_type=None):
        domain = []
        if material_type:
            domain.append(('material_type', '=', material_type))
        materials = request.env['material'].sudo().search(domain)
        return materials.read(['material_code', 'material_name', 'material_type', 'material_buy_price', 'supplier_id'])

    @http.route('/materials', type='json', auth='public', methods=['POST'])
    def create_material(self, **kwargs):
        if 'material_code' not in kwargs or 'material_name' not in kwargs or 'material_type' not in kwargs or \
           'material_buy_price' not in kwargs or 'supplier_id' not in kwargs:
            return {'error': 'Missing required fields'}
        
        if float(kwargs['material_buy_price']) < 100:
            return {'error': 'Material Buy Price must be at least 100'}
        
        material = request.env['material'].sudo().create(kwargs)
        return {'success': True, 'id': material.id}

    @http.route('/materials/<int:material_id>', type='json', auth='public', methods=['PUT'])
    def update_material(self, material_id, **kwargs):
        material = request.env['material'].sudo().browse(material_id)
        if not material.exists():
            return {'error': 'Material not found'}
        
        material.sudo().write(kwargs)
        return {'success': True}

    @http.route('/materials/<int:material_id>', type='json', auth='public', methods=['DELETE'])
    def delete_material(self, material_id):
        material = request.env['material'].sudo().browse(material_id)
        if not material.exists():
            return {'error': 'Material not found'}
        
        material.sudo().unlink()
        return {'success': True}
