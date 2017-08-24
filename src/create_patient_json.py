
from help_functions import write_obj_to_json_file, get_path


patient_1 = {
    "type": "patient",

    "personal": {
        "birthDate": "25. 08. 1995",
        "firstName": "Marko",
        "lastName": "Zeman",
        "address": {
            "street": "TKS",
            "houseNumber": "15",
            "city": "Ljubljana",
            "country": "Slovenia",
            "postCode": "1000"
        }
    },

    "health": {
        "temperature": "35.9",
        "heartRate": "50",
        "systolic": "115",
        "diastolic": "75",
        "spO2": "99",
    }
}


patient_2 = {
    "type": "patient",

    "personal": {
        "birthDate": "19. 09. 1950",
        "firstName": "Janez",
        "lastName": "Novak",
        "address": {
            "street": "Čopova ulica",
            "houseNumber": "25",
            "city": "Ljubljana",
            "country": "Slovenia",
            "postCode": "1000"
        }
    },

    "health": {
        "temperature": "36.4",
        "heartRate": "72",
        "systolic": "140",
        "diastolic": "88",
        "spO2": "98",
    }
}


patient_3 = {
    "type": "patient",

    "personal": {
        "birthDate": "17. 11. 1975",
        "firstName": "Ana",
        "lastName": "Horvat",
        "address": {
            "street": "Mariborska cesta",
            "houseNumber": "300",
            "city": "Maribor",
            "country": "Slovenia",
            "postCode": "2000"
        }
    },

    "health": {
        "temperature": "36.1",
        "heartRate": "66",
        "systolic": "133",
        "diastolic": "77",
        "spO2": "97",
    }
}


if __name__ == '__main__':
    path = '../' + get_path('data')

    write_obj_to_json_file(patient_1, path + 'MarkoZeman.json')
    write_obj_to_json_file(patient_2, path + 'JanezNovak.json')
    write_obj_to_json_file(patient_3, path + 'AnaHorvat.json')


