class lgn:
        """LOGIN"""
        email = "testkpcmanual+3@gmail.com"
        password = "Edamama@123!"




class md:
        """MONGODB"""
        strConnectionStringScheme = 'edamamaprecluster-pl-0.lmbse.mongodb.net/'
        strDatabaseName = 'edamamaprod_db'
        strPemFilePath = 'C:\\edamama-pre-mongo-db-atlas-x509.pem'





class rsg:
        """REGISTRATION"""
        strEmail = "testapi04-automation@gmail.com"
        strPassword = "test123"
        strFirstName = "QA API"
        strLastName = "Automation Test"
        boolIsPolicyChecked = True




class add:
        """ADDRESS"""
        addAddress = {
                "firstName": "QA API",
                "lastName": "Automation Test",
                "fullName": "QA API Automation Test",
                "phoneNumber": "9171234567",
                "regionName": "METRO MANILA",
                "regionId": "5dc5309b73a7ecd817f5b781",
                "cityName": "MANDALUYONG CITY",
                "cityId": "609fc3a7b1380627d48c7519",
                "cityRegionId" : "5dc5309b73a7ecd817f5b781",
                "zipCode": "3023",
                "barangayName": "BARANGKA DRIVE",
                "barangayId": "62cd49f8aefc154907c8a066",
                "barangayCityId": "609fc3a7b1380627d48c7519",
                "landmark":  "SMDC Light Residences",
                "buildingNumber": "",
                "country": "Philippines",
                "isDefault": False
        }

class plp:
    """PRODUCT LISTING"""
    
    intPriceFilterMin = 1
    
    intPriceFilterIncrement = 250
    
    intPriceFilterMax = 2500
    
    strBrand = 'Tiny Buds'
    
    diapering = {
                "strCategoryName": "Diapering", 
                "strCategoryId": "6091f6d349accc5190ff9c0f"
            }
    fashion = {
                "strCategoryName": "Fashion", 
                "strCategoryId": "6181ff6f18243a000d4787b1"
            }
    foodAndNutrition = {
                "strCategoryName": "Food and Nutrition", 
                "strCategoryId": "624d2856703ede70cc8f33e6"
            }
    nursery = {
                "strCategoryName": "Nursery", 
                "strCategoryId": "5f5b916383aef5605833ab61"
            }
    feedingAndMealtime = {
                "strCategoryName": "Feeding and Mealtime", 
                "strCategoryId": "5f5b916283aef5605833aae9"
            }
    mama = {
                "strCategoryName": "Mama", 
                "strCategoryId": "5f5b916383aef5605833ab49"
            }
    babyGear = {
                "strCategoryName": "Baby Gear", 
                "strCategoryId": "5f5bba0ef94f40316af06ca5"
            }
    homeAndLiving = {
                "strCategoryName": "Home and Living", 
                "strCategoryId": "5f5b916283aef5605833ab20"
            }
    toysAndLearning = {
                "strCategoryName": "Toys and Learning", 
                "strCategoryId": "5f5b916283aef5605833aafb"
            }
    bathAndBody = {
                "strCategoryName": "Bath And Body", 
                "strCategoryId": "5fbbc38a5d0c6d6c13672032"
            }
    furmama = {
                "strCategoryName": "Furmama", 
                "strCategoryId": "629762ec9e4154c20443fc6b"
            }
    beautyAndWellness = {
                "strCategoryName": "Beauty and Wellness", 
                "strCategoryId": "6445fff871d87188731ac829"
            }
    
    anko = {
                "strCategoryName": "Anko", 
                "strCategoryId": "anko-1670811910934"
        }
    
    
    
    
    
    class src:
        """SEARCH"""

        searchTerm = 'diaper'
        
        top30SearchTerms = ['unilove', 'mustela', 'littledragon', 'pampers', 'cetaphil', 'kleenfant', 'yoboo', 'big brute', 'diaper', 'cuddly', 'wipes', 'stroller',
                        'avent', 'aveeno', 'pigeon', 'eq', 'bearbrand', 'surf', 'huggies', 'nivea', 'dove', 'vaseline', 'cetaphil baby', 'unilove wipes', 'bear brand',
                        'hegen']
        
        oneWaySynonyms = [{"input": "bean essential", "synonyms": ['bean essentials',
                                                                   'essentials'
                                                                   ]
                           },
                   {"input": "moosegear", "synonyms": ['moose gear',
                                                       'Moose Gear'
                                                       ]
                    },
                   {"input": "littledragon", "synonyms":['little dragon',
                                                         'Little Dragon'
                                                         ]
                    },
                   {"input": "diaper", "synonyms":['diapers',
                                                   'Diapers'
                                                   ]
                    },
                   {"input": "unilove", "synonyms":['uni-love',
                                                    'airpro',
                                                    'Airpro baby diaper',
                                                    'Uni-love'
                                                    ]
                    },
                   {"input": "apple crumby", "synonyms":['applecrumby',
                                                         'Applecrumby'
                                                         ]
                    },
                   {"input": "hotwheel", "synonyms":['hot wheels',
                                                     'Hot wheels'
                                                     ]
                    },
                   {"input": "clothing", "synonyms":['dress',
                                                     'rompers',
                                                     'jean',
                                                     'boy clothing'
                                                     ]
                    },
                   {"input": "mommy poko", "synonyms":['mamypoko',
                                                       'Mamypoko'
                                                       ]
                    },
                   {"input": "fashion", "synonyms":['clothing',
                                                    'fashion',
                                                    'wear'
                                                    ]
                    },
                   {"input": "lunalove", "synonyms":['LunaLoveMNL'
                                                     ]
                    },
                   {"input": "pet care", "synonyms":['furmama'
                                                     ]
                    },
                   {"input": "pet soap", "synonyms":['furmama'
                                                     ]
                    }]
        
        synonym = [{"set1": ['v-tech',
                            'vtech',
                            'v tech'
                            ],
                    "set2": ['baby flow',
                           'flow',
                           'newborn flow'
                           ],
                    "set3": ['nipples',
                            'teats',
                            'teat'
                            ],
                    "set4": ['milk',
                            'milk drink',
                            'milk powder',
                            'baby milk'
                            ],
                    "set5": ['nipples',
                            'teats',
                            'teat'
                            ],
                    "set6": ['diaper',
                            'diaper pants',
                            'cloth diaper',
                            'baby diaper'
                            ],
                    "set7": ['twin',
                            '2-pack',
                            '2 pcs'
                            ],
                    "set8": ['walker',
                            'walkers',
                            'baby walker',
                            'baby walkers'
                            ],
                    "set9": ['bottles',
                            'bottle',
                            'feeding',
                            'feeding bottle'
                            ],
                    "set10": ['bear brand',
                            'bearbrand'
                            ],
                    "set11": ['booster seat',
                            'booster seats',
                            'booster car seat',
                            'booster car seats'
                            ],
                    "set12": ['stroller',
                            'strollers'
                            ],
                    "set13": ['High Chair',
                            'high chairs',
                            'highchair',
                            'highchairs'
                            ],
                    "set14": ['car seats',
                            'car seat',
                            'carseats',
                            'carseat'
                            ],
                    "set15": ['fashion',
                            'clothing',
                            'clothes'
                            ],
                    "set16": ['stuff',
                            'stuffed'
                            ],
                    "set17": ['changing pad',
                            'changing table',
                            'changing mat'
                            ],
                    "set18": ['babywearing',
                            'wraps',
                            'ring slings',
                            'hip seats'
                            ],
                    "set19": ['junior',
                            'jr'
                            ],
                    "set20": ['uni-love',
                            'unilove',
                            'unilove diaper',
                            'Uni-love'
                            ],
                    "set21": ['eq',
                            'e q'
                            ],
                    "set22": ['chair',
                            'seat'
                            ],
                    "set23": ['xxl',
                            'extra extra large',
                            'very very big'
                            ],
                    "set24": ['xl',
                            'extra large',
                            'very big',
                            'ex el'
                            ],
                    "set25": ['mom',
                            'nanay'
                            ],
                    "set26": ['shirt',
                            't-shirt'
                            ],
                    "set27": ['watch',
                            'watches'
                            ]
                    }]





class tss:
        """TRUE SPLIT SHIPMENT TD FOR E2E"""
        strReferralCode = "QA20231031080638813920-2"
        intPaymentMethod = 2
        
        whNasalAspiratorTravelCase = {
                "listName": "nosefrida-nosefrida-aspirator-w-travel-case-1575350160432",
                "prodId": "5de5ef90b6447b50049eb286",
                "variantId": "5dec931f5d5c9c6d17a78ea3"
        }
        whMagicUnicorn = {
                "listName": "tala-toys-tala-tiles-magnetic-tiles-triangles-set-48piece-1649733744417",
                "prodId": "663b1362cbcbab18c9f2cb88",
                "variantId": "663b1374e16c0c79bfbf68be"
        }
        whBabyNasalAspirator = {
                "listName": "tiny-buds-baby-nasal-aspirator-1585030934577",
                "prodId": "5e79a716cb032a3a516aa88b",
                "variantId": "5e79a74b7c5876bce1a13f93"
        }
        whHandsoap300mlRefillPouch = {
                "listName": "unilove-handsoap-300ml-refill-pouch-1658715111069",
                "prodId": "62ddfbe7d2f0c27156b8f1f4",
                "variantId": "62ddfc057bcbea5b0d591975"
        }
        whAfterBitesNaturalSoothingGel = {
                "listName": "tiny-buds-after-bites-natural-soothing-gel-50ml-1585027038957",
                "prodId": "5e7997de572f95ce55a0d20f",
                "variantId": "5f093f69c58b2e57e2764308"
        }
        whTssWhProductA = {
                "listName": "tss-product-a-1716171746289",
                "prodId": "664ab3e28206beb7c2c12f3a",
                "variantId": "664ab5176e08f1e7ab859a6f"
        }
        whTssWhProductB = {
                "listName": "tss-wh-product-b-1716172042369",
                "prodId": "664ab50a6e08f1e7ab859a5d",
                "variantId": "664ab5176e08f1e7ab859a6f"
        }
        whTssWhProductC = {
                "listName": "tss-wh-product-c-1716172120205",
                "prodId": "664ab558c84b9e6fc3c3cce3",
                "variantId": "664ab564dc547b40c17e6161"
        }
        whTssWhProductE = {
                "listName": "tss-wh-product-e-1716172244383",
                "prodId": "664ab5d4bc9594aed6b3ca9d",
                "variantId": "664ab5ebdc547b40c17e61cb"
        }
        whTssWhProductF = {
                "listName": "tss-wh-product-f-1716172384598",
                "prodId": "664ab66086fce3d202126e68",
                "variantId": "664ab686bc9594aed6b3caf7"
        }
        whSnsAutoProd = {
                "listName": "tsns-automation-product--please-do-not-update-or-delete-1698982294073",
                "prodId": "65446996bb20f86572e28d93",
                "variantId": "654469a7e414e585fe8649bc"
        }
        whSnsBabyDryTapedJumboLarge = {
                "listName": "baby-dry-taped-super-jumbo-large-2pack-2-x-68pcs--subscription-1658894664980",
                "prodId": "62e0b9485c52803d08827792",
                "variantId": "62e0cf2e38d84df35cc1a1a2"
        }
        scTssScProductM= {
                "listName": "tss-sc-product-m-1716173524214",
                "prodId": "664abad46e08f1e7ab859c71",
                "variantId": "664abae06e08f1e7ab859c92"
        }
        scTssScProductN= {
                "listName": "tss-sc-product-n-1716173612380",
                "prodId": "664abb2c1cf02bf66729fa12",
                "variantId": "664abb3c1cf02bf66729fa32"
        }
        scTssScProductO= {
                "listName": "tss-sc-product-o-1716173683506",
                "prodId": "664abb738206beb7c2c131a1",
                "variantId": "664abb7fdc547b40c17e632b"
        }
        scTssScProductP= {
                "listName": "tss-sc-product-p-1716173751898",
                "prodId": "664abbb7dc547b40c17e6361",
                "variantId": "664abbc486fce3d2021270e8"
        }
        scTssScProductQ= {
                "listName": "tss-sc-product-q-1716173809492",
                "prodId": "664abbf1dc547b40c17e637e",
                "variantId": "664abbff6e08f1e7ab859d15"
        }
        scTssScProductR= {
                "listName": "tss-sc-product-r-1716173876592",
                "prodId": "664abc3486fce3d2021271cd",
                "variantId": "664abc478206beb7c2c1321d"
        }