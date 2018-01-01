# url type : 0 = related , 1 absolute

perm_dic = {
    "crm.can_access_my_course": {"url_type": 0,
                                 "url": "student_my_classes",  # url name
                                 "method": "GET",
                                 "args": []
                                 },
    "crm.can_access_customer_list": {"url_type": 1,
                                     "url": "/king_admin/crm/customer/",
                                     "method": "GET",
                                     "args": []
                                     },
    "__crm.can_access_customer_detail": {"url_type": 0,
                                         "url": "table_obj_change",
                                         "method": "GET",
                                         "args": []
                                         },
    "crm.can_access_studyrecords": {"url_type": 0,
                                    "url": "study_records",
                                    "method": "GET",
                                    "args": []
                                    },
    "crm.can_access_homework_detail": {"url_type": 0,
                                       "url": "homework_detail",
                                       "method": "GET",
                                       "args": []
                                       },
    "crm.can_upload_homework": {"url_type": 0,
                                "url": "homework_detail",
                                "method": "POST",
                                "args": []
                                },
    "crm.access_kingadmin_table_obj_detail": {"url_type": 0,
                                              "url": "table_obj_change",
                                              "method": "GET",
                                              "args": []
                                              },
    "crm.change_kingadmin_table_obj_detail": {"url_type": 0,
                                              "url": "table_obj_change",
                                              "method": "POST",
                                              "args": [],
                                              "hooks": ["func1" and "func2"]
                                              },
                    }
