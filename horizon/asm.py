import base64
import zlib
import sys

# # 11-bit address range (2048 words capacity)
# rom_bp_placeholder = '55555'
# rom_bp_capacity = 2048
# rom_bp_string = '0eNrtXdtuHEeW/Jd+XWpQec8UMAN4xjPAvuwPLAaCLLXsxvKGVtNYwdC/b5OSRbrZmedCOSs3EfMwgCyySHVkRVRFRp74bfPT5d32dr+'\
#     '7Pmxe/7bZvbu5/rh5/d+/bT7ufr5+e3n/3w6fbreb15vdYXu1udhcv726/9P77bvd++3+1bubq592128PN/vN54vN7vr99n83r83nC/I'\
#     'C9z/o8Pb6cP4K9vO/Lzbb68PusNt++X0e/vDpzfXd1U/b/fFHfLvQ2/3u8MvV9rB79/RSF5vbm4/H7765vv8Njld0wf4lXGw+bV57H48'\
#     '/6PjzD/ubyzc/bX95++vu+B3HL3u81JvjX79/+PaP93/xYbf/eHjz7F/0625/uDv+l2+/y5eveLXc/0s+bu+v8eb3f+fm9XKxubnd7t9'\
#     '++aU2/3H8tpu7w+2d4ML/ufn8+cvvfr199+23M/f/t9++f/o57Y5/MuX4pbv9u7vd4eHPxw/1+M228tX2+Rd/vsfx5IO38g/edfvgzRg'\
#     'fvF0kH7w5/eKLP/y14+Hi5Lj4brjYQXAxL7oh/oiL5+Hi5biEbri4QXCxElxcG5fAwyXIcYndcPGD4OIkuPg2LpGHS5TjkrrhEgbBxUt'\
#     'wCW1cEg+XJMcld8MlDoJLkOAS27hkHi5ZjkvphksaBJcowSW1cSk8XIoYl7h0wyUPgkuS4JLbuJiFB8z910mRMd2QKYMgkyXIFAIZw0R'\
#     'G/lIf+73U/zAIMqKX+uc3xQk0zLd+I3/tj/1e+/8+BjRO9tpPvPcb5ou/kb/5x35v/v8YBBrRm78hXv0N893fyF/+Y7+X/x8HgUb08m+'\
#     'It3/DfP038vf/2O/9/5+DQCN6/zeEAWCYDoCRWwCxnwXwr0GgEVkA7LsitTZ4zrxKPr6ypMrn/vU6L/vQ3/2yffc/my8/4esnfk/oN1e'\
#     '3b/cPv9rrzV8VH/n21+3+0+GX3fXPX659++n4a95dH9582N9cvdldHy+2eX3Y320lwMT7rauf99vt9TMUTh6qTRszpgFgshAzsxpmy6i'\
#     'YPX+mrkGYTiE82awROUCGsBpON/BMbQkU4RJ4fGvKf+YS2F1/uPn/sQIMYS6c7uiZ6gp5/pUnKyS/YG+wtgDsIlwAbq0FMCptP7/VLpp'\
#     'bh/UFoLgSfxOyugCMcAH4tRaAHXQBUPettd+LAc5cib/bWV0AVrgAwloLwI26AAwBm2MvAPmV+Nuq1QXghAsgrrUA/KgLwBKwefYCkF+'\
#     'Jv39bXQBeuADSWgsgjLoAHAFbYC8A+ZX4G8XVBRCECyCvtQDiqAvAE7BF9gKQX4m/I11dAFG4AMpaCyCNugACAVtiLwD5lfhb39UFILT'\
#     'vniQOOi+APOoCiARsmb0A5Ffi77BXF4DQC3wSbOi8AMqoC4Aw+GxhLwD5lQQb+dUVILQC42pWoBnVC3x+Z140t/kbS0B+JUFgoLYEnNA'\
#     'MjOuZgaO6gZbw8BzbDVRcSRBMqC4BoR0YV7MDzah+oKN8fLYfqLiSIABRXQJCQzCuZgiaUR1BR/h4ju0IKq4kCFpUl4DQEoyrWYJmVE/'\
#     'QEU6eY3uCiisJAh3VJSA0BeNqpqAZ1RUU3OWyu5hp6zl5Us1/M3bC8ifHod7fHM4GouIfA1F/+5sCza8JkhpW5zGoHylgZ3LOovDorV1'\
#     't3+/url5tL4+/0P4Ixe3N5badjcp/CYKdaOK90djq76g4o7V0Wynn8/P+O6yThzUouaOJ17IQiEXjCHMvcG9txeEtszJg9zz9FLEf/ut'\
#     'HBWRf+F+CWd0vZaYwKhCoo1PVz/+7CORXXh0/ORVSVQ898eKT3EvykKdX88RRl8Q8T+HVWarOK2JU8yTk+hMS4YZ4kRviiHNnnnnuzKv'\
#     'DU50RH9UrCUXNAV5kflD3uGceZ/PqtFRnxEe1RuJSR5zwOrws/USckvNcVlfHozojPqoTEuvvvZ6wNrzI2vDU3B3u4B11Hqoz4qMaH7F'\
#     '+DMIT+SYvyjd54kyfZ55e8uoAVGfER80/RVdHnAg0eVGgyRNHBT3zqKBXJ546Iz5q4Cn6OuKEyeFFCSZPTCHyzDFEXh1x6oz4qAmnGOq'\
#     'IE5ElL4oseWK+kWeeb/TqTFNnxEeNNMX6iVRPeM1elFHyxHFGzxyd5NUZpt4OzKimXGyYcpT5LcokeeLcZGAOZQrqzFJvyEd13WLddfO'\
#     'E6xZErpsnXLfAdN2COqPUG/JRbbdYt90CYbsFke0WCNstMG23oM4k9YZ8VN8t1X23QPhuQeS7BcJ3C0zfLagzSL0hH9V4S3XjLRDGW5C'\
#     'dMySMt8A03oI6c9Qb8lGdt1R33oR3MfcuDc1ehmZuxPwebnmG2ofd5WG7r9RJNFMHD5/g/Un6+1eKb6USx89k9/HN/S/x4e3lx+3LwgN'\
#     'nP4b4kjzG8X7ZvN/tv/w+X438FYJX7nvkM5qRmu8SvErMHHNI0qVp/6yluTxZmuH+f0ThSbOl4ux1rOg6tnodJ7qOq17Hi67jq9cJouu'\
#     'E6nWi6Dqxep0kuk6qXieLrpOr1ymi65T6OlxEF/qhfiHZiv57/UKyJf2P+oVka/rH+oVki/qf9QvJVvW/6heKD1ypHFZWJc4sJU4H4gR'\
#     'xgjhBnHMSp2ceoQ5FSpwexAniBHGCOCclTubggbhIiTOAOEGcIE4Q56TEyRzXEY2UOCOIE8QJ4gRxTkqczM2haKXEmUCcIE4QJ4hzUuJ'\
#     'kjoaKTkqcGcQJ4gRxgjgnJU7mQLXopcRZQJwgThAniHNS4mTOOovSiHFcQJwgThAniHNS4mQeSohRSpwGxAniBHGCOCclTubI5ig9ORR'\
#     'xcgjECeIEcc5KnMyTQ1F6ciji5BCIE8QJ4pyUOAPz5FCUnhyKODkE4gRxgjhnJU7myaEkPTkUcXIIxAniBHHOSpzMk0NJenIo4uQQiBP'\
#     'ECeKclTiZJ4eS9ORQxMkhECeIE8Q5K3EyTw4lpy5MdX2n+47aspQbY9uJzhSqPzMRLU1l+Z79molocSrM8ofk1Y2rnZfUqDVOpT4jPBF'\
#     'VbUlU1ZaIqrbErGpLQV252hnyUXucSr2rjWKBJOpqo+7yxOxqS1HdudoZ8lGLnEq9uisRZW1JVNaWiLK2xCxrS0ldutoXcjtqkVOpFzk'\
#     'loq0tidraEvHkkZhtbSmrW1c7Qz5qkVOpPx4moq4tieraElHXlph1bamoa1c7Qz5qkZNZGs9vRF9bFj3SJ6KvLTMf2fOiLl7tjLkbFvP'\
#     'GAxzxmpdFhW2JeI3LzMK2bNTVq50x98NiXn+Cy0RjWxY1tmWisS0zG9uyVZevdsY8DIt5/REuE5VtWVT2lInKtswsg8pOXb/aGfM4LOb'\
#     '1Z7hMdLZlUWdbJjrbMrOzLXt1/2pnzEe14IypP8NlwoPLIg8uEx5cZnpwOagLWDtjnofFvP4MlwkTLotMuEyYcJlpwuWobmDtjHkZFvP'\
#     'GMxzhwmWRC5cJFy4zXbic1BWsfTF3y7CYN57hCBsui2y4TNhwmWnD5azuYO2MuRkW88YznOw+5t6nRd906RFJQiQJkSREkmaKJHErgsu'\
#     'ijiTFvmI37AaEteoASSEMDePy90yYFMLxePbjanJbjL4fFXILuYXcQm7nkltmArhYdVyzs9wOu/dr675hIfYBi2h/oBD7gIW5P1CcvhM'\
#     'XYgmxhFhCLOcSS2ZfRPHqoHtnsRw2NGN9XSyJd88i2mSjXi0Lc5OtBH0PMsQSYgmxhFjOJZbMjpCiPyLUWSyHTRvaejqhUIdDRT5toQ5'\
#     '/cm3YpO++hlhCLCGWEMu5xJLZC1Oy+nBlZ7EcNqZtY10siViXWUTnrgqR63p2uapcFn3jOeQScgm5hFzOJZfMNqAHhlWeTO+sl8MecbH'\
#     '1GHTJlF6Kzi+WTOkl8wCjWYy+6R6CCcGEYEIw5xLMwhVMq57r0Vkwhz0faHNVMM+8QJ5KnCjpc+YNkrheXTLFYZ8CyYRkQjIhmXNKZl6'\
#     '4kunVY5E6S+awx6ttaUgmddRkiTLJpM6SLJErmdLIz5PhSJBMSCYkE5I5l2QarmRG9VS5vpLph51O4ZaGZHpKMrNMMj0lmZkrmdLgz5P'\
#     'ZcpBMSCYkE5I5l2RarmRm9VDOzpI57HAfZxqSSUV/zCKTTCr7YxauZIr7xTEhCJIJyYRkziqZzAlBDxSrnGncWTKHHRHkbEMyqfSPsTL'\
#     'JpOI/hhv/MeKCZEz5gWRCMiGZs0qm50qmVY+E7yyZw475cfUxP2deIk8lThb/MVT8x3DjP0Ya/4mY9QPJhGRCMmeVzMCVTK9u1OgsmcM'\
#     'O+3G+IZlU/MfI4j+Giv8YbvzHiOM/mPgDyYRkQjJnlczIlUx9IVFnyRx25I8LDcmk4j9GFv8xVPzHcOM/Rhz/wdwfSCYkE5I5q2QmrmR'\
#     'mdZ9bZ8kcdvCPiw3JpOI/Vhb/MVT8x3LjP0Yc/8HsH0gmJBOSOatkcmf/2EVdh9lZMoed/eNSQzKFL5Hcd0T7GN652r7f3V292l4ef9f'\
#     '97t2r25vL7bkDtU9OB/2ueJx/nounqhy426XW6ms7E1QZqgxVhirPpMqFOy3BOn0DI5gTzAnmBHPOxZzcE4DW6+v4wJxgTjAnmHMu5uS'\
#     'm2u0LutnAnGBOMCeYcy7m5Ca1bNQXdYE5wZxgTjDnXMzJ3n1M+s4mMCeYE8wJ5pyKOc+W552nzqxv7wF1gjpBnaDOyaiTvUdU9C0uoE5'\
#     'QJ6gT1DkZdXI3idyib/MAdYI6QZ2gzsmok7tL5Iy+1QHUCeoEdYI6J6NO7jaRs/rp/qBOUCeoE9Q5F3Ua7jaRc/op76BOUCeoE9Q5GXV'\
#     'yt4mc10/7BnWCOkGdoM7JqJO9TfSCqc+gTlAnqBPUORl1sreJon76L6gT1AnqBHVORp3sbaKknwIL6gR1gjpBnXNRp2VvEwknpz+Z1Fn'\
#     '6joHNo46BDfWykUI1WrpCfEEQVV4WqvHy9OdVR7i6IlwXbq11UYZdF43xwI5qB/eyifqOagf33In6XjgX+skYtb7Ah2VY4EsDeOqG90Y'\
#     'GfKGAN1zgjRD4sBbwZlTgo6kD7ykp8FYEvKeo3lsu8MJW6ydDbDoDb4cFvtFq/fyGPgXKyYA3FPCOC7wTAp/WAn7YOvPYKJrzVDerl9W'\
#     'Ze6qb1XPn83thKe+TCQKdgR+2lDc2Hu6e39CnQAUZ8I4CPnCBD0Lgy1rAD1stGRsPd56qlvSyNmZPVUt6bhuzl3aKLmsBP2xBWmo93AU'\
#     'K+CQDPlDAJy7wSQi8WQv4YWt+UuvhjmrG87IeIE8143luUZCXViKuZeyFYY291Hq4SxTwRQZ8ooDnOnde6NzFtZy7MKxzl1oPd5RzF2T'\
#     'Onaecu8B17oK00W0t5y4O69yl1sMdadXLnDtPOXeB69wFoy6M7wz8sM5dbjzcBcq5CzLnLlDOXeA6d8Gqa487Az+sc5cbD3eBcu6CzLk'\
#     'LlHMXuM5dcOryzs7AD+vc5cbDnfSGZt+vXrvZHm1X2IYV6BxfsKcaiJc1u8hwt+RPsNRPqC+VoK5QvfduEGlDpA2RNkTaJoq0OW4aOER'\
#     'tdKmzyo77NtTwPwK1xxFkjmeg9jgC1/EMSd2dC8mEZEIyIZmzSWbhSmbWhj47S+a4PlJuSCa1SRhlWwbUW+az69Uls6hLkyGZkExIJiR'\
#     'zMsn03INTcdHG5TtL5rgOfGOzNVBebhRa9NQue+Qas9Go27IhmZBMSCYkczbJNFzJVB806iyZw546KEtdMiMVU4my4yaRiqlE7nGT6NQ'\
#     '16ZBMSCYkE5I5m2RyRxFHrz2i2Vkyhz2vVRrJzkid0Iyy81qROqEZuee1ojj+kyCZkExIJiRzVsl0XMmM2sPtnSVz2JOuxTYkk4r/RFn'\
#     '8J1Lxn8iN/0Rx/CdDMiGZkExI5qySyW1tiFk7FqSzZA47I6A0jpFFKv6TZPGfSMV/Ejf+E8XxnwLJhGRCMiGZs0pmYEpmWrQDlTpL5rD'\
#     'TVYpvSCYV/0my+E+k4j+JG/9J0vjPE+AhmZBMSCYkczLJ5BZcJasdRddZMoedS1UaMysSFf9JsvhPouI/iRv/SeImcgPJhGRCMiGZs0p'\
#     'm4kqm1w7x7D3KYNiJQaUxMShR+Z8ky/8kKv+TuPmfJO5RxvgfaCY0E5o5rWZyx/+kqJ1/3Fszh53/UxrzfxIVAEqyAFCiAkCJGwBK4hZ'\
#     'YzP+BZkIzoZnTaiZ3/k/K2tHxvTVz2AFApTEAKFEJoCxLACUqAZS5CaAkTQBFDACCZkIzoZmzambgDgDKi7Z1o7dmDjsBqDQmACUqApR'\
#     'lEaBERYAyNwKUxREgTACCZkIzoZnTaiZ3AlBWFxb11sxRRwDZpTECKFMZoCzLAGUqA5S5GaAszgBhBBA0E5oJzZxWM7kjgLLXdr311sw'\
#     'wrGY2ZgAJXyP5b4niBA8m+EDxoHhQvGkVjzvBJ0d996EDdYI6QZ2gzrmokzvJJb+gAw/UCeoEdYI6J6NO7vHknPVdaKBOUCeoE9Q5GXV'\
#     'yj9zkou/EAnWCOkGdoM65qDNyU6Rl0XcjgTpBnaBOUOdk1MkNRhSj78gBdYI6QZ2gzsmok7tNVKy+KwXUCeoEdYI6J6NO7jZRcfrODFA'\
#     'nqBPUCeqcjDq520TF67sTQJ2gTlAnqHMu6kzsbaKgn6EP6gR1gjpBnZNRJ3ubKOpHqYM6QZ2gTlDnZNTJ3iZ6wURtUCeoE9QJ6pyMOtn'\
#     'bRFk/WBnUCeoEdYI6J6NO9jZR0c/XBXWCOkGdoM65qDMzt4nssujHrII6QZ2gTlDnZNRpudRp9PM6QZ2gTlAnqHMy6vRc6hS2OjwZ1xn'\
#     '6TqiOo06oNo32wEA07trFEV9gimjGdSAqeZ/9QEv9QFtdOk64dNxaSyeNunRsvRDk4c5sLx1RIciz61nqenXghVPtnwxb6wx8HhZ42wC'\
#     'eooQlyICn7vjT69WBD0Lgw1rAl2GB9w3gSbGIMuBJLYhc4KMQ+LgS8HYZFvjYAD5QwCcZ8IECPnGBT0Lg01rAm2GBzw3gIwV8lgEfKeA'\
#     'zF3hhq/iTIQOdgR+1Vdy61sNdooAvMuATBTz7qb4IgS9rAe+GBb71cJep971FBnymXueYdfIPXyjqqlrWAn7YfkfXergrFPBGBnyhgDd'\
#     'c4I0QeLMW8MOWlLnGw51ZKOBFLWZnbmjienXgpY2ua3l/dljvzzUe7p7f0KdAORnwhgLecYEXOndxLefODuvc+cbDnaGcOyNz7gzl3Bm'\
#     'uc2ekfZRrOXd2WOfONx7uDGnmy5w7Q3r1XOfOCJ27uJZzZ4d17nzj4c5Qzp2ROXeGcu4M17kzUd3a3hd4N6xz51sPd5RzZ2TOnaGcO8N'\
#     '17kxSVw93Bn5Y5863Hu6ENzT7fs36/syIKBOiTIgyIco0U5TpTA6iRp1FHWXKfRVv2C2L8JI8iqX8jhi/b2DFUoZI5KquXfTVq1BdqC5'\
#     'UF6o7meo6pupao06BdlbdYfeLg2m8Z1Lbhla4iUBtG1ruJoK1+s5daCY0E5oJzZxMM7mHbqxTB+g7a+awUZvQ2IYjX0StbBuOfM+03G0'\
#     '46/Vly9BMaCY0E5o5mWYGrmbqzx511sxhU4rBNTSTiq5Y2Ua2paIrlruRbaO+ZRuaCc2EZkIzJ9PMyNXMpD622Vkzhw14h0bqz1LhLys'\
#     '7xGWp8JflHuKyWV+vDs2EZkIzoZmTaWbiamZRn3jvrJnDno0JoaGZ1MFnJzsGaamDz457DNKJM0AZmgnNhGZCM2fVTObU/weOVQ4L6ay'\
#     'Zwx4rDI1DRpbKADlZBshSGSDHzQA5cQaoQDOhmdBMaOasmlm4munUc5Y6a+awJ7JDqmumozJATpYBclQGyHEzQE6aAXoyaAmaCc2EZkI'\
#     'z59JMw61IckE9oq6vZvphh1mExkwDR2WAnCwD5KgMkONmgJw0A/RkRh00E5oJzYRmTqaZhquZST3ds7NmDjsHKJSGZlIZICfLADkqA+S'\
#     '4GSAnbjHHJCFoJjQTmjmtZnInCbmiHozcWTOHnSQUG5OEHJUB8rIMkKMyQJ6bAfLiDmbMAYJmQjOhmdNqJncOkDfqmfKdNXPYOUCxMQf'\
#     'IURkgL8sAOSoD5LkZIC/NAEXMAYJmQjOhmdNqJncOkHfqOo7OmjnsHKDYmAPkqQyQl2WAPJUB8twMkBdngDAHCJoJzYRmTquZ3DlAXt9'\
#     'k1Fkzh50DFBtzgDyVAfKyDJCnMkCemwHy4gwQ5gBBM6GZ0MxpNZM7B8gndQlcZ80cdg5QbMwB8lQGyMsyQJ7KAHluBsiLM0CYAwTNhGZ'\
#     'CM6fVTO4cIF/U/ZmdNXPYOUCxMQdI+hrJfUsMi74/s0DxoHhQPCjeXIrHnUgQjL4EEdQJ6gR1gjrnok7LPWQXXtCFB+oEdYI6QZ2TUSc'\
#     '3Nx6cvhIN1AnqBHWCOiejTm4UKnh9MxaoE9QJ6gR1Tkad3N29EPQFSaBOUCeoE9Q5GXWyt4mivicH1AnqBHWCOueiTsfeJkr6uhRQJ6g'\
#     'T1AnqnIw62dtEWd+aAeoEdYI6QZ2TUSd7m6joyxNAnaBOUCeoczLq5G4TxUU/Qx/UCeoEdYI6J6NO7jZRNPpR6qBOUCeoE9Q5F3V67jZ'\
#     'RfMFEbVAnqBPUCeqcjDq520TR6QcrgzpBnaBOUOdk1MndJopeP18X1AnqBHWCOiejTvY2UdCPWQV1gjpBnaDOyaiTvU0UZWNWH8d1JtN'\
#     '3zGoedcxqblRgGao2MsrmsBqqNjJyB7VG4Uz6x2GDvYEvwwLf6HGJkQI+i4A/vZ6lrlcHPguB9ysBfz9KeFDgG2UEkSpXj7IygkiVq0d'\
#     'uGUEUTtR+HPTUG3gzLPCNidrPb+gToNIiAz4TwJ9erwp8WoTAx7WAt8MCHxvAUxqfjAx4SuOT4QIv7AR/HLLRG/hhO8FzqgP//IY+Bcq'\
#     'KgH9+QxPXqwNvhcDntYAfttg25wbwVLFtkpXBJ6rYNnHL4JOw0fjxgHNv4IdtZ8ylAbylgPcy4C0FvOcC74V1KctawA9bMVaWBvBULWe'\
#     'SVVknqpYzcausk7SP1awF/LA9OcU0gPcU8FEGvKeAj1zghc5dXMu5C8M6d6Xh3CWqVDDJnLtElQomrnOXpG2Sazl3YVjnrjScu0Q5d0n'\
#     'm3CXKuUtc5y4Jnbu4lnMXh3XuSsO5S5Rzl2TOXaKcu8R17lLRdq73Bn5Y5640nLtEOXdZ5twlyrnLXOcuL9ri4N7AD+vclYZzlyjnLsu'\
#     'cu0Q5d5nr3GWjbb/sDfywzl1pOHfCG5p/v1p1+2WyCCIhiIQgEoJIUwWRYmQGkbJTt1+COkGdoE5Q52zUyY2/Z69uvwR1gjpBnaDO2ag'\
#     'zc6kzqNsvQZ2gTlAnqHM26uSeHMpR3X4J6gR1gjpBnZNR57kDHuepM6nbL0GdoE5QJ6hzNurkzubMWd1+CeoEdYI6QZ2zUaflUmdRt1+'\
#     'COkGdoE5Q52zUyR1rXBZ1+yWoE9QJ6gR1zkadnkudRt1+CeoEdYI6QZ2zUSd3Inyx6vZLUCeoE9QJ6pyNOrmniYpTt1+COkGdoE5Q52z'\
#     'UyT1NVLy6/RLUCeoEdYI6Z6NO7mmiEtTtl6BOUCeoE9Q5G3VyTxOVqG6/BHWCOkGdoM7JqDNzTxOVpG6/BHWCOkGdoM7ZqPPsaaJ/Hy9'\
#     '32F4df95Pl3fb2/3u+HMuNr8eSe6BG4/f5VOxKblUQvafP/8fzvm0NA=='

# 32x64-value cell ROM, for loading into 64-value cell RAM module
rom_bp_placeholder = lambda i: str((i + 10000) * 1000 + 123)
rom_bp_capacity = 2048
rom_bp_string = '0eNrNnd1uHVeSpV9F0NVMt1XY8R9hYC7mr8tTXV1V46nxzXTDoCXaIloiBYqy2yj43Sd5ZJTFTebJk7lXiuyLRlkWwyRPM'\
    'k4w4ltr/e35d28+nL+7vri8ef7l356/On//8vri3c3F1eXzL5+7vvjxbPrXz77+8788++ni5vWz/3Tx7B+fUZv+7z8/+4fD/7j9Z5ZnZ++'\
    'fnT179+bs5fnrqzevzq+fffzA76+un928Pn92+7E/XV2/+t2/Xv7r5T9Nf/ju+uqH67O3by8uf/hY+erDzfuLV+fPbq6u3rz/3fMvnl+8v'\
    'Lp8//zL//e35+8vfrg8e3P76d38/O58+rx+vLi++TD9yRfPL8/e3v7Bx7/xwp//Mn3c5avz/3j+Jf3yxYqP1E8+kld95NeffKSs+sg/f/K'\
    'R+su/ffH8/PLm4ubi/OMXffiHn7+9/PD2u/Pr6cv5+0fffltuzi5vXry8evvdxeXZzdX1VPrd1fuLj6/a355P9V4o/c6+eP7z9L+oxe9s+'\
    'i+9urg+f/nxr+gXt1Vurq/efPvd+euzHy+mEtPHfX/x5ub8euX3/OXr85f/fvuVvLz6cPsMtU9egX87/PHl5cf/7vvbanT7/364Pj+//PS'\
    'rvHj1/Euf/u7F9csPFzeHf7z96F9uv5/dN4LXfiP0t2+EHr4RsC/995982dOPAvn0g7Dx+fuqKxWfllr3QP6vrlR+WmrdE/qHrlR9WkpXl'\
    'frnu6W4fVrKVpX6Y1eKPi3lq0q9u7j8964af1otVlX7U1dKPi2V63vDJ6X001K1qtRfulJ25yltq2r9767W3See1jfOT2rdeeRp3TP/f7p'\
    'ad555WvfQ/7Wrdeehp3VP/f+9W0vuPPW07rH/pqt157Enn2221+ev+lYrn/TV23+2mV4ra3ut7dZr292vvrXtvZa6UrS913JXirf3WulKy'\
    'fZeq10p3d5rrStl23utd6V8e6ONrlRsb7TZlcrtjba6UjXQaP9r987bBhrtf+tq0UCj/e9dLR5otP+jqyUDjfZ/drV0oNH+U1fLtjdanmm'\
    'surax8nBjvbg5f/vbl/r6/OzHn19cXbx58d3Z9fX5m7tfsuZyd71b783FD69v5uvVcovt6n347vri5e335aF61pb77N16785vv1vnH96++'\
    'OHs/cM1abnh3q35/sOb7z9Mn+WLs5cXrx6uycud927Nn86mV/DhWrLceu/Wenn17t1U7OXZd2/Ou1q63Hvv1rq4vrp88f7m4mU3Lpstt94'\
    'HKv1wfnb94qfX5/e+SF9uv3fLnb99d/Pzw9+wOKH/dsXeTD/T0+c3vaa//iralcwT2vDdkmevfjy7fHn+aqZgndCLuyf5+url+fv3F5c/v'\
    'Phw2dfzdkI/7r7myx8uLs8fqkUn9OOHvn/Td2++KJ/QmO8W/f7Nz7df7PXVd1c3L76/vv3DuyVle3+2bhA+cQdha9u3gNv3T1dXr7pfB3h'\
    'ty355ddb9xIisbdPvb64uu5dDdG1vPnSEq+u+jq3tx7/2u/uVfG0X/nB9dnkxvVfcLxVrm/D12U8vvr94/7qrk5sa8Ls309tDV6nWNuBfv'\
    '00P1NK2tvu+v3ozvfV9/+HeGz6t7r3vb6Z3gwc/K17ddKcqt+9Vt28LXS1Z3W8/vst3ZXR1m/3u7Gb64f65q2PrW+x/vHszdZcfz993pXx'\
    '1Y315/eHV+fzMFiNj7922qjN91P/+ubw6n2ao22Hl+E77bhP9ZKPND7fUX8t+O/27Vxd//7S/v7h+f/Ptlg33x2Z/WHJPn+m7s+vDZ/rl8'\
    '/8yfdDVh5t3H1aUPf9xeh5uXk/vbR9rv/v528N3/9vvr6/efntxORV7/uXN9YfzX07/xh/OCA9u16l7SYj6t7q7/571/lvhF8955r/bV+O'\
    'FanO/F8XKN1apz7VwcoUtnNxgCyd32MLJA7Zw8oQtnLxgC6dosIVTEGzhFAxbOIXgFk6huIVTGG7hFI5bOEXgFk6RuIVT1PZ33pxprLm2s'\
    'ebnuppmg11Nk2BX02TY1TQFdjVNhV1N05BX03TY1TQDdjXNhF1Ns3BX02q4q2kR7mpajLualuCupqW4q2kNLPOjG2prptfW2l4bu2+Hyse'\
    '3QxWA7VAlZjtUBdoOUWuo7RA1gmyHqDFoO0RNYNshagraDlEz2HaImsO2Q9QCsR2ilpDtELVCbYeIGnY7REQjM2q3imgzjZTa2k7qn/NMS'\
    'sTQMymRQM+kRAo/kxIZ/ExK5LAzKVHAzqRECTqTEhXyTErcYGdSYkKfSYkZeyYlFuiZlFhhZ1Jiw59JiR19JiUe2OfX4vJ4poHTugW/2FN'\
    'Z8NMTXfDfvld+cSI/f/c1k1ULfT++zydZ9x+b2/fTbzT/2fXFzeu357eD2fFnRNY+I79VBj0m789v63z729PyYnpcrqY3kbNfdTP/sOFp+'\
    'bX6mmdBVp1o5MSXRAZeEvvML8n52cvXD74i7e4L8o9bfnwPtde8Hnz8h+L+kezo68ULP4JzR1X6DS58e/7q9hfVv7/fvJtmu4deP3pgbN7'\
    'yBM4+UzYAkvOedz02R9312AJ112NL1F2PrVB3PfaGuuuxE+qux86oux67oO567Iq667Eb7K7H7rC7HnvA7nrsCbvrsRfsrsfRYHc9joGdy'\
    'eFvP9hafUAPyXte9jgYddnjENRlj0NRlz0OQ132OBx12eMI4GWPI1GXPY5CXfY4G+qyx0mwyx4nwy57nAK77HEq7LLHabDLHqfDLnucA/s'\
    'N6jlwmrvtUQy0W9mz3ZIqqt2SGqrdkjqq3ZIGqt2SJqrdkhaw3ZI1VLslI1S7JWNUuyUTWLslU1i7JTNYuyVzWLslC1i7JUtYuyUbgNSov'\
    'wDy7OIgBxYHsufigDhRiwPiQi0OSBpqcUBCqMUBCaMWBySCWhyQKGpxQGKoxQGJoxYHJAFbHJAkbHFAUrDFAWmDLQ5ICbY4IGXY4oB0QOF'\
    'IMddaa0DEyLtgapw5jKlx1jimxtUgmBoXgTA1LkZhalwCwdS4FISpcRkMU+NyEKbGFTBMjSthmBpXITA1aQ2CqUkjFKYmjbGYmjQZWrl2U'\
    '+ocp8ZtwM6Dd+fUpCmUU5NmUE5NmsM5NWkB59SkJYxTk1YwTk2ogTg1IUJyakIM49SEBM2pCSmWUxMyKKcm5DBOTSjwnJpQojk1oZHFQg+'\
    'qsZxoKkoDHVz2J43DsaRxBJY0jsSTxlF40jgbjjROwpHGySjSOAVKGqfiSOM0OGmcDiaNM7CkcSaONM7agTSuBieNa4BzYD7Bh+LBDs4D6'\
    'wzZZZ1B3obXGeQ0vs4gZ8g6g1xQqjtXmOrODaO6c0ep7jxwqjtPlOrOC6e6i4ZT3QVBVHfBGNVdCEx1FwpW3YUNLYK7zjrbSmWrLRM/smp'\
    'Dn6hqg+dVG/ff3zrrrFWyjfs+S8erzd1dWbc+AvLIjwA/1UeAtgp3WIDCHT6R2GcbMIzZFSsVgcVsiMBiNkRgMRsisJgNUVjMhigyZkMUF'\
    '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'\
    'qR8AXHoE89RHY7q+/L1EaDEu7D4al3QfD0u6DYWn3wbC0+2Bk2n0wLO0+GJZ2HwxLuw/Gpd2H4NLuQ3Bp9yG4tPsQXNp9CC7tPmRg5vL+f'\
    'hSz96Pt9vr7KqOiKYxxagZjnJrDGKcWMMapJYxxagVjnKjBGCciGONEDGOcSHCMEymOcSLDMU7kOMaJAsc4UeIYJxrASX3OXd9je2fdlR5'\
    'NYVRnTRFUZ01RVGdNMVRnTXFUZ00JVGdNSVRnTSlUZ01tqM6aSrDOmsqwzpoqsM6aqrDOmmqwzprqsM6aIzmdnnOdNbdvCHZVQeWIj/5XX'\
    'alCbQhyxEf/D10pQm0IcsRH/49dKQFuCHLESv9PXSlDbQhyxEr/L12pgG0IcshK/+uuVsE2BDlkpf/XrhbBNgQ5ZKX/TVdrgFfy/ioTs1e'\
    'Z7d76n4EwDcPG1odhY+vD8LH1YfjY+jBcbH0YLrY+DBVbHwaNrQ/HxdaHw2Prw8Gx9eHY2PpwXGx9+A6x9eHw2PrwgXE42gluag818Nhur'\
    'b+T2CrEhwGlkBgHlEISAiiFFAhQCm0oQCmUIIBSKIMApVCBAUqhCgKUQg0GKIU6DFAKDQSgFJoQQCm0UIBSWMMCSmE0tMHtYJU5+5Wg7Z1'\
    '0J9TTdRz1dAOgnu4Y1NMDhXp6wlBPLwzqGQ2FegbhUM9gFOoZgkM9Q3GoZxgE9QzHoJ4RMNQzEox6jmShem+tEnOQV/D2pcJnUD2tN7s/r'\
    'npab3x/XPW03gN/WfW03g9/WfW03hl/XvW03hp/XvW00R7/AdXTenv8o6qn9Q7586qnDR75S6qnDVb5x1VPG/zyj6qeNhjnzwqUtpjnL6q'\
    'eNtjoL6meRoz0455F+4mqp9joq//4rD49VVD7iK/+Aqgdq0BtWwC140RQOzb66j8+qy9P9BG4HZdmHoFYeARq1SMQC49AnfoIDPjq+46ME'\
    'zVG0aNTKRQ9OpVC0aNTKRQ9OpVC0aNTKRQ9Sk1Q9OhUCkWPTqVQ9OhUCkaPTrVg9OhUC0aPTrVg9OhUC0aPTrVg9OhUa+A35pjz1Y8BX33'\
    'fkXGipigV1FQKpYKaSqFUUFMplApqKoVSQU2lgCqoqRpKBTWVQqmgDgGBGMbpkMQGYpwO6aggxukQKAlinKZaMBXUVAumgppqwVRQU62RX'\
    '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'


def generate_bp(program: list[int]) -> str:
    length = rom_bp_capacity
    while len(program) < length:
        program.append(0)

    b64_string = rom_bp_string[1:]
    bin_string = base64.b64decode(bytes(b64_string, 'utf-8'))

    json = zlib.decompress(bin_string)
    t = str(json)[2:-1]
    
    for i in range(length):
        if type(rom_bp_placeholder) == str:
            t = t.replace(rom_bp_placeholder, str(program[i]), 1)
        else:
            t = t.replace(rom_bp_placeholder(i), str(program[i]), 1)

    z = zlib.compress(bytes(t, 'utf-8'), level=9)
    b = '0' + str(base64.b64encode(z))[2:-1]

    return b


## Opcodes
opcodes = {
    'ADD':    [0, 128],
    'SUB':    [1, 129],
    'MUL':    [2, 130],
    'DIV':    [3, 131],
    'MOD':    [4, 132],
    'EXP':    [5, 133],
    'LSH':    [6, 134],
    'RSH':    [7, 135],
    'AND':    [8, 136],
    'OR':     [9, 137],
    'NOT':    [10, 138],
    'XOR':    [11, 139],
    'BCAT':   [12, 140],
    'HCAT':   [13, 141],
    'ADDS':   [16, 144],
    'SUBS':   [17, 145],
    'MULS':   [18, 146],
    'DIVS':   [19, 147],
    'MODS':   [20, 148],
    'EXPS':   [21, 149],
    'LSHS':   [22, 150],
    'RSHS':   [23, 151],
    'ANDS':   [24, 152],
    'ORS':    [25, 153],
    'NOTS':   [26, 154],
    'XORS':   [27, 155],
    'BCATS':  [28, 156],
    'HCATS':  [29, 157],
    'JEQ':    [32, 160],
    'JNE':    [33, 161],
    'JLT':    [34, 162],
    'JGT':    [35, 163],
    'JLE':    [36, 164],
    'JGE':    [37, 165],
    'JNG':    [38, 166],
    'JPZ':    [39, 167],
    'JVS':    [40, 168],
    'JVC':    [41, 169],
    'JMP':    [42, 170],
    'NOOP':   [43],
    'STORE':  [48, 176],
    'LOAD':   [49],
    'STOREI': [50, 178],
    'LOADI':  [51],
    'STORED': [52, 180],
    'LOADD':  [53],
    'PUSH':   [56, 184],
    'POP':    [57]
}

# Numbers must be replaced with the argument of that index
builtin_macros = {
    'HALT': [['JMP', 'PC']],
    'RESET': [['XOR', 'SP', 'SP'], ['JMP', '#0']],
    'CMP': [['SUBS', 'NIL', 1, 2]],
    'INC': [['ADD', 1, '#1']],
    'INCS': [['ADDS', 1, '#1']],
    'DEC': [['SUB', 1, '#1']],
    'DECS': [['SUBS', 1, '#1']],
    'CALL': [['ADD', 'LR', 'PC', '#2'], ['JMP', 1]],
    'RETURN': [['JMP', 'LR']],
    'MOV': [['ADD', 1, 'NIL', 2]],
    'MOVS': [['ADDS', 1, 'NIL', 2]],
    'MOV16': [['PUSH', 2], ['POP', 1]]
}

preprocessor = [
    'CONST',
    'DEFINE',
    'INCLUDE',
    'REP',
    'END'
]

sections = [
    'DATA',
    'MACRO',
    'PROGRAM'
]

registers = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'AR': 12,
    'SP': 13,
    'LR': 14,
    'PC': 15,
    'NIL': 255
}

debug = 0
lines = []
lineinfo = []
lineaddr = []
labels = {}
consts = {}
errors = 0
program_reached = 0
curr_section = 0
repeat = 0
repeat_line = 0
code = []
machine_code = []
code_info = []


def syntax_error(msg: str, i: int):
    print(f'Syntax error on line {i}: {msg}')
    global errors; errors += 1

def lexical_error(msg: str, i: int, hint_label: bool = False):
    if not hint_label:
        print(f'Unknown token on line {i}: {msg}')
    else:
        print(f'Malformed label on line {i}: {msg}')
    global errors; errors += 1
    
def instr_to_machine_code(c: list, i: int) -> list:
    if c[0] in ['NOOP']:
        c = opcodes[c[0]][0] << 24
        return c
    
    # Comments show byte order of operands, for IMM16 the blank byte immediately to the back or front (when the last byte is not blank)
    #   is the LSB or MSB respectively
    # RN is the first register operand
    # RM is the second register operand
    # RD is the destination register, and synonymous with RN where RN is ommitted
    # IMM8 and IMM16 are immediate values of 8 and 16 bits respectively
    
    # OP RD RN RM
    # OP RD RN IMM8
    if c[0] in ['ADD', 'MUL', 'AND', 'ORR', 'XOR', 'ADDS', 'MULS', 'ANDS', 'ORRS', 'XORS', 'SUB', 'DIV', 'MOD', 'EXP', 'LSH', 'RSH', 'SUBS', 'DIVS', 'MODS', 'EXPS', 'LSHS', 'RSHS', 'BCAT', 'HCAT', 'BCATS', 'HCATS']:
        # RN = RD
        if len(c) < 4:
            c.insert(1, c[1])
        
        # c = [OP, RD, RN, RM/IMM8]
        
        if len(c) < 4:
            syntax_error(f'too few arguments', code_info[i])
            return c
        elif len(c) > 4:
            syntax_error(f'too many arguments', code_info[i])
            return c
        
        if type(c[1]) != int:
            syntax_error('expected register as destination', code_info[i])
            return c
        if type(c[2]) != int:
            syntax_error('expected register as first operand', code_info[i])
            return c
        
        if type(c[3]) == int:
            t = 0
        else:
            t = 1
            c[3] = int(c[3][1:], base=0)
            if c[3] < -128 or c[3] > 127:
                syntax_error(f'literal "#{c[2]}" out of range [-128, 127]', code_info[i])
                return c
        
        c[0] = opcodes[c[0]][t]
        
        c = c[0] << 24 | c[1] << 16 | c[2] << 8 | c[3] & 0xFF
        return c
    
    # OP RD RN _
    if c[0] in ['NOT', 'NOTS']:
        # RN = RD
        if len(c) < 3:
            c.insert(1, c[1])
        
        # c = [OP, RD, RN, RM/IMM8]
        
        if len(c) < 3:
            syntax_error(f'too few arguments', code_info[i])
            return c
        elif len(c) > 3:
            syntax_error(f'too many arguments', code_info[i])
            return c
        
        if type(c[1]) != int:
            syntax_error('expected register as destination', code_info[i])
            return c
        if type(c[2]) != int:
            syntax_error('expected register as operand', code_info[i])
            return c
        
        t = 0
        
        c[0] = opcodes[c[0]][t]
        
        c = c[0] << 24 | c[1] << 16 | c[2] << 8
        return c
    
    # OP _ RN _
    # OP _ IMM16 _
    if c[0] in ['JMP', 'JEQ', 'JNE', 'JLT', 'JGT', 'JLE', 'JGE', 'JNG', 'JPZ', 'JVS', 'JVC', 'PUSH', 'STORE', 'STOREI', 'STORED']:
        # c = [OP, RN/IMM16]
        
        if len(c) < 2:
            syntax_error(f'too few arguments', code_info[i])
            return c
        elif len(c) > 2:
            syntax_error(f'too many arguments', code_info[i])
            return c
    
        if type(c[1]) == int:
            t = 0
        else:
            t = 1
            c[1] = int(c[1][1:], base=0)
            if c[1] < -32768 or c[1] > 32767:
                syntax_error(f'literal "#{c[1]}" out of range [-32768, 32767]', code_info[i])
                return c
        
        c[0] = opcodes[c[0]][t]
        
        c = c[0] << 24 | (c[1] << 8 if t == 0 else c[1] & 0xFFFF)
        return c

    # OP RD _ _
    if c[0] in ['LOAD', 'POP', 'LOADI', 'LOADD']:
        # c = [OP, RD]
        
        if len(c) < 2:
            syntax_error(f'too few arguments', code_info[i])
            return c
        elif len(c) > 2:
            syntax_error(f'too many arguments', code_info[i])
            return c

        if type(c[1]) != int:
            syntax_error('expected register as destination', code_info[i])
            return c
        
        c[0] = opcodes[c[0]][0]
        
        c = c[0] << 24 | c[1] << 16
        return c
    
    return c

def macro_to_instr(c: list):
    o = c[0]
    out = []
    
    for i in builtin_macros[o]:
        ins = i.copy()
        for j, a in enumerate(ins):
            if type(a) == int:
                ins[j] = c[a]
                
        out.append(ins)
    
    return out

def interpret_instr(c: list, i: int):
    # Instructions
    if c[0] in opcodes:
        if curr_section != 0:
            syntax_error('instruction not allowed outside ".PROGRAM" section', lineinfo[i])
            return
        machine_code.append(c)
        code_info.append(lineinfo[i])
    
    # Built-in macro instructions
    elif c[0] in builtin_macros:
        if curr_section != 0:
            syntax_error('instruction not allowed outside ".PROGRAM" section', lineinfo[i])
            return
        new_code = macro_to_instr(c)
        for d in new_code:
            machine_code.append(d)
            code_info.append(lineinfo[i])

    else:
        syntax_error(f'unkown instruction "{c[0]}"')

def repeat_block(c: list, i: int):
    if len(c) < 2:
        syntax_error(f'"{c[0]}" must be followed by a non-negative integer', lineinfo[i])
        return
    if len(c) > 2:
        syntax_error(f'"{c[0]}" takes only one non-negative integer as an argument', lineinfo[i])
        return
    
    try:
        n = int(c[1])
        if n < 0:
            raise ValueError
    except:
        syntax_error(f'"{c[0]}" must be followed by a non-negative integer', lineinfo[i])
        return
    
    # Get code until END is found
    r = []
    ended = 0
    counters = []
    for j in range(i + 1, len(code)):
        if code[j][0] == '@END':
            ended = 1
            break
        
        # @{s, i} blocks are counters: s=start value, i=increment value
        len_counters = -1
        while len_counters < len(counters):
            len_counters = len(counters)
            
            for k, a in enumerate(code[j]):
                k_ = 0
                s_, i_ = 0, 0
                if a.startswith('@{'):
                    if len(a) > 2:
                        s_ = int(a[2:])
                    else:
                        k_ += 1
                        s_ = int(code[j][k + k_])
                    k_ += 1
                
                    if code[j][k + k_].endswith('}'):
                        i_ = int(code[j][k + k_][:-1])
                    else:
                        i_ = int(code[j][k + k_])
                        k_ += 1
                    
                    counters.append((s_, i_))
            
                    # remove counter block and replace with string format ('{i}') placeholder
                    while k_ >= 0:
                        code[j].pop(k + k_)
                        k_ -= 1
                    code[j].insert(k, f'({len(counters) - 1})')

        r.append(code[j])
        
    if not ended:
        # This error will be detected while parsing the rest of the code inside the first pass
        return
    
    for j in range(n):
        ri = [e.copy() for e in r]
        for k, rk in enumerate(r):
            for l, a in enumerate(rk):
                if a.startswith('(') and a.endswith(')'):
                    index = int(a[1:-1])
                    ri[k][l] = '#' + str(counters[index][0])
                    updated_ctr = (counters[index][0] + counters[index][1], counters[index][1])
                    counters.pop(index)
                    counters.insert(index, updated_ctr)

        for k, rk in enumerate(ri):
            interpret_instr(rk, k)

    return

if __name__ == '__main__':
    # arg 0 = program name
    # arg 1 = input
    # arg 2 = output filename (default print to stdout)
    
    if len(sys.argv) not in (2, 3):
        print(f"Usage: python {sys.argv[0]} <input_file> <optional_ouput_file>")
        exit(1)
    
    ## First pass
    # Read source lines into lines array
    with open(sys.argv[1], 'r') as fd:
        lines = [l.strip().upper() for l in fd.readlines()]
        lineinfo = [i + 1 for i in range(len(lines))]
    
    # Strip comments and empty lines, replace commas with spaces
    lines = [line.split(';')[0].replace(',', ' ').strip() for line in lines]
    
    indices = [i for i, l in enumerate(lines) if len(l) == 0]
    while len(indices):
        lineinfo.pop(indices[-1])
        lines.pop(indices[-1])
        indices.pop()
    
    # Split lines into tokens
    code = [l.split() for l in lines]
    
    # Identify tokens and translate
    errors = 0
    for i, c in enumerate(code):
        
        # REP..END blocks are interpreted when REP is found, discard instructions until END is found
        if repeat:
            if c[0] == '@END':
                repeat = 0
            continue
        
        # Preprocessor directives
        if c[0][0] == '@' and c[0][1:] in preprocessor:
            if c[0] == '@REP':
                repeat = 1
                repeat_line = lineinfo[i]
                if curr_section != 0:
                    syntax_error(f'"{c[0]}" only allowed in ".PROGRAM" section', lineinfo[i])
                    continue
                repeat_block(c, i)
                continue
            elif c[0] == '@END':
                syntax_error(f'"{c[0]}" without a corresponding "@REP"', lineinfo[i])
                continue
            
            if curr_section != 1:
                syntax_error('preprocessor directives not allowed outside ".MACRO" section, except "@REP"', lineinfo[i])
                continue
            if c[0] == '@CONST':
                if len(c) != 3:
                    syntax_error(f'"{c[0]}" must be followed by an identifier and a value', lineinfo[i])
                    continue
                else:
                    if c[1] in opcodes or c[1] in builtin_macros or c[1] in preprocessor or c[1] in sections or c[1] in registers:
                        syntax_error(f'"{c[0]}" name may not be a reserved word', lineinfo[i])
                        continue
                    elif c[1] in consts:
                        syntax_error(f'"{c[0]}" "{c[1]}" defined multiple times', lineinfo[i])
                    consts[c[1]] = c[2]
            elif c[0][1:] in ['DEFINE', 'INCLUDE']:
                # TODO
                syntax_error(f'"{c[0]}" is reserved but has not been implemented', lineinfo[i])
                continue
            else:
                syntax_error(f'unkown preprocessor directive "{c[0]}"')
                continue
            
        # Sections
        elif c[0][0] == '.' and c[0][1:] in sections:
            if program_reached:
                syntax_error('sections cannot be declared after ".PROGRAM" section begins', lineinfo[i])
                continue
            elif c[0][1:] == 'PROGRAM':
                program_reached = 1
                curr_section = 0
            elif c[0][1:] == 'MACRO':
                curr_section = 1
            elif c[0][1:] == 'DATA':
                # TODO
                curr_section = 2
                syntax_error(f'"{c[0]}" is reserved but has not been implemented', lineinfo[i])
                continue
            else:
                syntax_error(f'unkown section "{c[0]}"')
                continue
        
        # Labels
        elif c[0][-1] == ':' or len(c) > 1 and c[1] == ':':
            l = c[0].strip(':')
            if l in opcodes or l in builtin_macros or l in preprocessor or l in sections or l in registers:
                syntax_error(f'label may not be a reserved word', lineinfo[i])
                continue
            elif l in consts:
                syntax_error(f'"{l}" was already defined as a "@CONST"', lineinfo[i])
                continue
            elif l in labels:
                syntax_error(f'"{l}" defined multiple times', lineinfo[i])
                continue
            
            labels[l] = len(machine_code)
        
        # Instructions and Built-in macros
        elif c[0] in opcodes or c[0] in builtin_macros:
            interpret_instr(c, i)
            program_reached = 1
            
        # Everything not picked up is a lexical error, hint at labels ending in ':'
        else:
            lexical_error(c[0], lineinfo[i], True)
    
    if repeat:
        syntax_error('"@REP" without a corresponding "@END"', repeat_line)
    
    if debug:
        print('## FIRST PASS ##')
        for c in machine_code:
            print(c)
        print()
        print(labels)
        print(consts)
        print('## END FIRST PASS ##')
        print()
        
    if errors:
        print(f'{errors} error{"s" if errors > 1 else ""} detected')
        exit(0)
    
    ## Second pass
    # Jump to start
    if 'START' in labels and labels['START'] != 0:
        machine_code.insert(0, ['JMP', 'START'])
        code_info.insert(0, 0)
        for l in labels:
            labels[l] += 1
    
    # Data load instructions
    # TODO
    
    # Convert consts and labels into #constants
    for k in consts:
        consts[k] = '#' + str(consts[k])
    for k in labels:
        labels[k] = '#' + str(labels[k])
    
    cg = consts.get
    lg = labels.get
    for i, instr in enumerate(machine_code):
        machine_code[i] = [cg(op, op) for op in instr]
    for i, instr in enumerate(machine_code):
        machine_code[i] = [lg(op, op) for op in instr]
    
    # Convert register names to numbers
    rg = registers.get
    for i, instr in enumerate(machine_code):
        machine_code[i] = [rg(op, op) for op in instr]
    
    # All leftover strings should be literals starting with '#'
    e = []
    for i, instr in enumerate(machine_code):
        e += [(tok, i) for tok in instr if tok not in opcodes and type(tok) == str and tok[0] != '#']
    for tok, i in e:
        try:
            n = int(tok)
            syntax_error(f'number literals must start with "#"', code_info[i])
        except:
            lexical_error(tok, code_info[i])
    
    if debug:
        print('## MID SECOND PASS ##')
        for c in machine_code:
            print(c)
        print()
        print(labels)
        print(consts)
        print('## END MID SECOND PASS ##')
        print()
    
    # Convert instructions into machine code
    for i, instr in enumerate(machine_code):
        # print(instr)
        machine_code[i] = instr_to_machine_code(instr, i)
        if (not errors):
            machine_code[i] = machine_code[i] - 2 * (machine_code[i] & (1 << 31))
    
    ## Output
    if errors:
        print(f'{errors} error{"s" if errors > 1 else ""} detected')
        exit(0)
    
    if debug:
        print('## SECOND PASS ##')
        for c in machine_code:
            print(c)
        print('## END SECOND PASS ##')
    
    ## Third pass
    bp = generate_bp(machine_code)
    
    if len(sys.argv) == 3:
        with open(sys.argv[2], 'w') as fd:
            fd.write(bp)
    else:
        print(bp)