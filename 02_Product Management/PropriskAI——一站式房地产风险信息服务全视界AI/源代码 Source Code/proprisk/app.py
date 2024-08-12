from random import randint
from flask_cors import CORS
from flask import Flask, request, jsonify
from pymongo import MongoClient


from proprisk.util.chatUtil import generate_real_estate_introduction, generate_supplier_introduction
from proprisk.mapper.supplier_data import search_supplier_nonmember, generate_supplier_data_format
from proprisk.api.user import user_api, token_required
from proprisk.api.real_estate import real_estate_api
from proprisk.mapper.real_estate_data import search_real_estate_nonmember, generate_data_format

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 禁止中文转义
CORS(app, supports_credentials=True)

app.register_blueprint(user_api, url_prefix='/user_api')
app.register_blueprint(real_estate_api, url_prefix='/real_estate_api')
app.config['SECRET_KEY'] = "114514"

client = MongoClient('mongodb://localhost:27017/')
db = client['user']
collection = db['user']


# test
@app.route("/realEstateSearch", methods=["POST"])
@token_required
def realEstateSearch(cur_user):
    data = request.get_json()
    realEstate = data.get('realEstate')
    if realEstate is not None:
        real_estate, impacted_suppliers_list, impacted_suppliers_info_list, error_message = \
            search_real_estate_nonmember(realEstate)
        if error_message is not None:
            return jsonify({'error': error_message})
        testData1, riskCauseData, LR_radio, real_estate_revenue, real_estate_profit, real_estate_cash_flow, real_estate_ROE = \
            generate_data_format(real_estate, impacted_suppliers_list, impacted_suppliers_info_list)
        realEstateDiscription = generate_real_estate_introduction(real_estate)
        profitData = [{'year': 2021, 'value': 10},
                      {'year': 2022, 'value': 20},
                      {'year': 2023, 'value': 40},
                      {'year': 2024, 'value': 60},
                      {'year': 2025, 'value': 90}, ]
        stockData = [{'year': 2021, 'value': 10.67},
                     {'year': 2022, 'value': 20.78},
                     {'year': 2023, 'value': 40.09},
                     {'year': 2024, 'value': 60.9},
                     {'year': 2025, 'value': 90.8}, ]
        return jsonify({'realEstateResult': testData1,
                        "realEstateDiscription": realEstateDiscription,
                        'riskCauseData': riskCauseData,
                        'LR_radio': LR_radio,
                        'real_estate_revenue': real_estate_revenue,
                        'real_estate_profit': real_estate_profit,
                        'real_estate_cash_flow': real_estate_cash_flow,
                        'real_estate_ROE': real_estate_ROE,
                        'profitData': profitData,
                        'stockData': stockData})


@app.route("/supplierSearch", methods=["POST"])
@token_required
def supplierSearch(cur_user):
    data = request.get_json()
    supplier = data.get('supplier')
    if supplier is not None:
        risklevel = randint(0, 100)
        supplier, real_estate_list, real_estate_affected_list, error_message = search_supplier_nonmember(supplier)
        print(error_message)
        if error_message is not None:
            return jsonify({'error': error_message})

        testData1, riskCauseData, affected_degree, supplier_revenue, supplier_profit, supplier_cash_flow, supplier_ROE \
            = generate_supplier_data_format(supplier, real_estate_list, real_estate_affected_list)
        supplierDiscription = generate_supplier_introduction(supplier)
        profitData = [{'year': 2021, 'value': 10},
                      {'year': 2022, 'value': 20},
                      {'year': 2023, 'value': 40},
                      {'year': 2024, 'value': 60},
                      {'year': 2025, 'value': 90}]
        stockData = [{'year': 2021, 'value': 10.67},
                     {'year': 2022, 'value': 20.78},
                     {'year': 2023, 'value': 40.09},
                     {'year': 2024, 'value': 60.9},
                     {'year': 2025, 'value': 90.8}]
        print(affected_degree[0]['value'])
        return jsonify({'supplierResult': testData1,
                        "supplierDiscription": supplierDiscription,
                        "riskLevel": risklevel,
                        'riskCauseData': riskCauseData,
                        'affected_degree': affected_degree,
                        'supplier_revenue': supplier_revenue,
                        'supplier_profit': supplier_profit,
                        'supplier_cash_flow': supplier_cash_flow,
                        'supplier_ROE': supplier_ROE,
                        'profitData': profitData,
                        'stockData': stockData})


if __name__ == '__main__':
    print('user_api=', user_api)

    app.config['SECRET_KEY'] = "114514"
    app.run(host='127.0.0.1', port=5000, debug=True)
