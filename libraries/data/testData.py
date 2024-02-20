class plp:
    """PRODUCT LISTING"""
    
    intPriceFilterMin = 500
    
    intPriceFilterIncrement = 8000
    
    intPriceFilterMax = 8000
    
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

        searchTerm = 'car seats'
        
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