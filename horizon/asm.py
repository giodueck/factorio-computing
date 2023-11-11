import base64
import zlib
import sys
import string

# 11-bit address range (2048 words capacity)
rom_bp_placeholder = '55555'
rom_bp_capacity = 2048
rom_bp_string = '0eNrtXdtuHEeW/Jd+XWpQec8UMAN4xjPAvuwPLAaCLLXsxvKGVtNYwdC/b5OSRbrZmedCOSs3EfMwgCyySHVkRVRFRp74bfPT5d32dr+'\
    '7Pmxe/7bZvbu5/rh5/d+/bT7ufr5+e3n/3w6fbreb15vdYXu1udhcv726/9P77bvd++3+1bubq592128PN/vN54vN7vr99n83r83nC/I'\
    'C9z/o8Pb6cP4K9vO/Lzbb68PusNt++X0e/vDpzfXd1U/b/fFHfLvQ2/3u8MvV9rB79/RSF5vbm4/H7765vv8Njld0wf4lXGw+bV57H48'\
    '/6PjzD/ubyzc/bX95++vu+B3HL3u81JvjX79/+PaP93/xYbf/eHjz7F/0625/uDv+l2+/y5eveLXc/0s+bu+v8eb3f+fm9XKxubnd7t9'\
    '++aU2/3H8tpu7w+2d4ML/ufn8+cvvfr199+23M/f/t9++f/o57Y5/MuX4pbv9u7vd4eHPxw/1+M228tX2+Rd/vsfx5IO38g/edfvgzRg'\
    'fvF0kH7w5/eKLP/y14+Hi5Lj4brjYQXAxL7oh/oiL5+Hi5biEbri4QXCxElxcG5fAwyXIcYndcPGD4OIkuPg2LpGHS5TjkrrhEgbBxUt'\
    'wCW1cEg+XJMcld8MlDoJLkOAS27hkHi5ZjkvphksaBJcowSW1cSk8XIoYl7h0wyUPgkuS4JLbuJiFB8z910mRMd2QKYMgkyXIFAIZw0R'\
    'G/lIf+73U/zAIMqKX+uc3xQk0zLd+I3/tj/1e+/8+BjRO9tpPvPcb5ou/kb/5x35v/v8YBBrRm78hXv0N893fyF/+Y7+X/x8HgUb08m+'\
    'It3/DfP038vf/2O/9/5+DQCN6/zeEAWCYDoCRWwCxnwXwr0GgEVkA7LsitTZ4zrxKPr6ypMrn/vU6L/vQ3/2yffc/my8/4esnfk/oN1e'\
    '3b/cPv9rrzV8VH/n21+3+0+GX3fXPX659++n4a95dH9582N9cvdldHy+2eX3Y320lwMT7rauf99vt9TMUTh6qTRszpgFgshAzsxpmy6i'\
    'YPX+mrkGYTiE82awROUCGsBpON/BMbQkU4RJ4fGvKf+YS2F1/uPn/sQIMYS6c7uiZ6gp5/pUnKyS/YG+wtgDsIlwAbq0FMCptP7/VLpp'\
    'bh/UFoLgSfxOyugCMcAH4tRaAHXQBUPettd+LAc5cib/bWV0AVrgAwloLwI26AAwBm2MvAPmV+Nuq1QXghAsgrrUA/KgLwBKwefYCkF+'\
    'Jv39bXQBeuADSWgsgjLoAHAFbYC8A+ZX4G8XVBRCECyCvtQDiqAvAE7BF9gKQX4m/I11dAFG4AMpaCyCNugACAVtiLwD5lfhb39UFILT'\
    'vniQOOi+APOoCiARsmb0A5Ffi77BXF4DQC3wSbOi8AMqoC4Aw+GxhLwD5lQQb+dUVILQC42pWoBnVC3x+Z140t/kbS0B+JUFgoLYEnNA'\
    'MjOuZgaO6gZbw8BzbDVRcSRBMqC4BoR0YV7MDzah+oKN8fLYfqLiSIABRXQJCQzCuZgiaUR1BR/h4ju0IKq4kCFpUl4DQEoyrWYJmVE/'\
    'QEU6eY3uCiisJAh3VJSA0BeNqpqAZ1RUU3OWyu5hp6zl5Us1/M3bC8ifHod7fHM4GouIfA1F/+5sCza8JkhpW5zGoHylgZ3LOovDorV1'\
    't3+/url5tL4+/0P4Ixe3N5badjcp/CYKdaOK90djq76g4o7V0Wynn8/P+O6yThzUouaOJ17IQiEXjCHMvcG9txeEtszJg9zz9FLEf/ut'\
    'HBWRf+F+CWd0vZaYwKhCoo1PVz/+7CORXXh0/ORVSVQ898eKT3EvykKdX88RRl8Q8T+HVWarOK2JU8yTk+hMS4YZ4kRviiHNnnnnuzKv'\
    'DU50RH9UrCUXNAV5kflD3uGceZ/PqtFRnxEe1RuJSR5zwOrws/USckvNcVlfHozojPqoTEuvvvZ6wNrzI2vDU3B3u4B11Hqoz4qMaH7F'\
    '+DMIT+SYvyjd54kyfZ55e8uoAVGfER80/RVdHnAg0eVGgyRNHBT3zqKBXJ546Iz5q4Cn6OuKEyeFFCSZPTCHyzDFEXh1x6oz4qAmnGOq'\
    'IE5ElL4oseWK+kWeeb/TqTFNnxEeNNMX6iVRPeM1elFHyxHFGzxyd5NUZpt4OzKimXGyYcpT5LcokeeLcZGAOZQrqzFJvyEd13WLddfO'\
    'E6xZErpsnXLfAdN2COqPUG/JRbbdYt90CYbsFke0WCNstMG23oM4k9YZ8VN8t1X23QPhuQeS7BcJ3C0zfLagzSL0hH9V4S3XjLRDGW5C'\
    'dMySMt8A03oI6c9Qb8lGdt1R33oR3MfcuDc1ehmZuxPwebnmG2ofd5WG7r9RJNFMHD5/g/Un6+1eKb6USx89k9/HN/S/x4e3lx+3LwgN'\
    'nP4b4kjzG8X7ZvN/tv/w+X438FYJX7nvkM5qRmu8SvErMHHNI0qVp/6yluTxZmuH+f0ThSbOl4ux1rOg6tnodJ7qOq17Hi67jq9cJouu'\
    'E6nWi6Dqxep0kuk6qXieLrpOr1ymi65T6OlxEF/qhfiHZiv57/UKyJf2P+oVka/rH+oVki/qf9QvJVvW/6heKD1ypHFZWJc4sJU4H4gR'\
    'xgjhBnHMSp2ceoQ5FSpwexAniBHGCOCclTubggbhIiTOAOEGcIE4Q56TEyRzXEY2UOCOIE8QJ4gRxTkqczM2haKXEmUCcIE4QJ4hzUuJ'\
    'kjoaKTkqcGcQJ4gRxgjgnJU7mQLXopcRZQJwgThAniHNS4mTOOovSiHFcQJwgThAniHNS4mQeSohRSpwGxAniBHGCOCclTubI5ig9ORR'\
    'xcgjECeIEcc5KnMyTQ1F6ciji5BCIE8QJ4pyUOAPz5FCUnhyKODkE4gRxgjhnJU7myaEkPTkUcXIIxAniBHHOSpzMk0NJenIo4uQQiBP'\
    'ECeKclTiZJ4eS9ORQxMkhECeIE8Q5K3EyTw4lpy5MdX2n+47aspQbY9uJzhSqPzMRLU1l+Z79molocSrM8ofk1Y2rnZfUqDVOpT4jPBF'\
    'VbUlU1ZaIqrbErGpLQV252hnyUXucSr2rjWKBJOpqo+7yxOxqS1HdudoZ8lGLnEq9uisRZW1JVNaWiLK2xCxrS0ldutoXcjtqkVOpFzk'\
    'loq0tidraEvHkkZhtbSmrW1c7Qz5qkVOpPx4moq4tieraElHXlph1bamoa1c7Qz5qkZNZGs9vRF9bFj3SJ6KvLTMf2fOiLl7tjLkbFvP'\
    'GAxzxmpdFhW2JeI3LzMK2bNTVq50x98NiXn+Cy0RjWxY1tmWisS0zG9uyVZevdsY8DIt5/REuE5VtWVT2lInKtswsg8pOXb/aGfM4LOb'\
    '1Z7hMdLZlUWdbJjrbMrOzLXt1/2pnzEe14IypP8NlwoPLIg8uEx5cZnpwOagLWDtjnofFvP4MlwkTLotMuEyYcJlpwuWobmDtjHkZFvP'\
    'GMxzhwmWRC5cJFy4zXbic1BWsfTF3y7CYN57hCBsui2y4TNhwmWnD5azuYO2MuRkW88YznOw+5t6nRd906RFJQiQJkSREkmaKJHErgsu'\
    'ijiTFvmI37AaEteoASSEMDePy90yYFMLxePbjanJbjL4fFXILuYXcQm7nkltmArhYdVyzs9wOu/dr675hIfYBi2h/oBD7gIW5P1CcvhM'\
    'XYgmxhFhCLOcSS2ZfRPHqoHtnsRw2NGN9XSyJd88i2mSjXi0Lc5OtBH0PMsQSYgmxhFjOJZbMjpCiPyLUWSyHTRvaejqhUIdDRT5toQ5'\
    '/cm3YpO++hlhCLCGWEMu5xJLZC1Oy+nBlZ7EcNqZtY10siViXWUTnrgqR63p2uapcFn3jOeQScgm5hFzOJZfMNqAHhlWeTO+sl8MecbH'\
    '1GHTJlF6Kzi+WTOkl8wCjWYy+6R6CCcGEYEIw5xLMwhVMq57r0Vkwhz0faHNVMM+8QJ5KnCjpc+YNkrheXTLFYZ8CyYRkQjIhmXNKZl6'\
    '4kunVY5E6S+awx6ttaUgmddRkiTLJpM6SLJErmdLIz5PhSJBMSCYkE5I5l2QarmRG9VS5vpLph51O4ZaGZHpKMrNMMj0lmZkrmdLgz5P'\
    'ZcpBMSCYkE5I5l2RarmRm9VDOzpI57HAfZxqSSUV/zCKTTCr7YxauZIr7xTEhCJIJyYRkziqZzAlBDxSrnGncWTKHHRHkbEMyqfSPsTL'\
    'JpOI/hhv/MeKCZEz5gWRCMiGZs0qm50qmVY+E7yyZw475cfUxP2deIk8lThb/MVT8x3DjP0Ya/4mY9QPJhGRCMmeVzMCVTK9u1OgsmcM'\
    'O+3G+IZlU/MfI4j+Giv8YbvzHiOM/mPgDyYRkQjJnlczIlUx9IVFnyRx25I8LDcmk4j9GFv8xVPzHcOM/Rhz/wdwfSCYkE5I5q2QmrmR'\
    'mdZ9bZ8kcdvCPiw3JpOI/Vhb/MVT8x3LjP0Yc/8HsH0gmJBOSOatkcmf/2EVdh9lZMoed/eNSQzKFL5Hcd0T7GN652r7f3V292l4ef9f'\
    '97t2r25vL7bkDtU9OB/2ueJx/nounqhy426XW6ms7E1QZqgxVhirPpMqFOy3BOn0DI5gTzAnmBHPOxZzcE4DW6+v4wJxgTjAnmHMu5uS'\
    'm2u0LutnAnGBOMCeYcy7m5Ca1bNQXdYE5wZxgTjDnXMzJ3n1M+s4mMCeYE8wJ5pyKOc+W552nzqxv7wF1gjpBnaDOyaiTvUdU9C0uoE5'\
    'QJ6gT1DkZdXI3idyib/MAdYI6QZ2gzsmok7tL5Iy+1QHUCeoEdYI6J6NO7jaRs/rp/qBOUCeoE9Q5F3Ua7jaRc/op76BOUCeoE9Q5GXV'\
    'yt4mc10/7BnWCOkGdoM7JqJO9TfSCqc+gTlAnqBPUORl1sreJon76L6gT1AnqBHVORp3sbaKknwIL6gR1gjpBnXNRp2VvEwknpz+Z1Fn'\
    '6joHNo46BDfWykUI1WrpCfEEQVV4WqvHy9OdVR7i6IlwXbq11UYZdF43xwI5qB/eyifqOagf33In6XjgX+skYtb7Ah2VY4EsDeOqG90Y'\
    'GfKGAN1zgjRD4sBbwZlTgo6kD7ykp8FYEvKeo3lsu8MJW6ydDbDoDb4cFvtFq/fyGPgXKyYA3FPCOC7wTAp/WAn7YOvPYKJrzVDerl9W'\
    'Ze6qb1XPn83thKe+TCQKdgR+2lDc2Hu6e39CnQAUZ8I4CPnCBD0Lgy1rAD1stGRsPd56qlvSyNmZPVUt6bhuzl3aKLmsBP2xBWmo93AU'\
    'K+CQDPlDAJy7wSQi8WQv4YWt+UuvhjmrG87IeIE8143luUZCXViKuZeyFYY291Hq4SxTwRQZ8ooDnOnde6NzFtZy7MKxzl1oPd5RzF2T'\
    'Onaecu8B17oK00W0t5y4O69yl1sMdadXLnDtPOXeB69wFoy6M7wz8sM5dbjzcBcq5CzLnLlDOXeA6d8Gqa487Az+sc5cbD3eBcu6CzLk'\
    'LlHMXuM5dcOryzs7AD+vc5cbDnfSGZt+vXrvZHm1X2IYV6BxfsKcaiJc1u8hwt+RPsNRPqC+VoK5QvfduEGlDpA2RNkTaJoq0OW4aOER'\
    'tdKmzyo77NtTwPwK1xxFkjmeg9jgC1/EMSd2dC8mEZEIyIZmzSWbhSmbWhj47S+a4PlJuSCa1SRhlWwbUW+az69Uls6hLkyGZkExIJiR'\
    'zMsn03INTcdHG5TtL5rgOfGOzNVBebhRa9NQue+Qas9Go27IhmZBMSCYkczbJNFzJVB806iyZw546KEtdMiMVU4my4yaRiqlE7nGT6NQ'\
    '16ZBMSCYkE5I5m2RyRxFHrz2i2Vkyhz2vVRrJzkid0Iyy81qROqEZuee1ojj+kyCZkExIJiRzVsl0XMmM2sPtnSVz2JOuxTYkk4r/RFn'\
    '8J1Lxn8iN/0Rx/CdDMiGZkExI5qySyW1tiFk7FqSzZA47I6A0jpFFKv6TZPGfSMV/Ejf+E8XxnwLJhGRCMiGZs0pmYEpmWrQDlTpL5rD'\
    'TVYpvSCYV/0my+E+k4j+JG/9J0vjPE+AhmZBMSCYkczLJ5BZcJasdRddZMoedS1UaMysSFf9JsvhPouI/iRv/SeImcgPJhGRCMiGZs0p'\
    'm4kqm1w7x7D3KYNiJQaUxMShR+Z8ky/8kKv+TuPmfJO5RxvgfaCY0E5o5rWZyx/+kqJ1/3Fszh53/UxrzfxIVAEqyAFCiAkCJGwBK4hZ'\
    'YzP+BZkIzoZnTaiZ3/k/K2tHxvTVz2AFApTEAKFEJoCxLACUqAZS5CaAkTQBFDACCZkIzoZmzambgDgDKi7Z1o7dmDjsBqDQmACUqApR'\
    'lEaBERYAyNwKUxREgTACCZkIzoZnTaiZ3AlBWFxb11sxRRwDZpTECKFMZoCzLAGUqA5S5GaAszgBhBBA0E5oJzZxWM7kjgLLXdr311sw'\
    'wrGY2ZgAJXyP5b4niBA8m+EDxoHhQvGkVjzvBJ0d996EDdYI6QZ2gzrmokzvJJb+gAw/UCeoEdYI6J6NO7vHknPVdaKBOUCeoE9Q5GXV'\
    'yj9zkou/EAnWCOkGdoM65qDNyU6Rl0XcjgTpBnaBOUOdk1MkNRhSj78gBdYI6QZ2gzsmok7tNVKy+KwXUCeoEdYI6J6NO7jZRcfrODFA'\
    'nqBPUCeqcjDq520TF67sTQJ2gTlAnqHMu6kzsbaKgn6EP6gR1gjpBnZNRJ3ubKOpHqYM6QZ2gTlDnZNTJ3iZ6wURtUCeoE9QJ6pyMOtn'\
    'bRFk/WBnUCeoEdYI6J6NO9jZR0c/XBXWCOkGdoM65qDMzt4nssujHrII6QZ2gTlDnZNRpudRp9PM6QZ2gTlAnqHMy6vRc6hS2OjwZ1xn'\
    '6TqiOo06oNo32wEA07trFEV9gimjGdSAqeZ/9QEv9QFtdOk64dNxaSyeNunRsvRDk4c5sLx1RIciz61nqenXghVPtnwxb6wx8HhZ42wC'\
    'eooQlyICn7vjT69WBD0Lgw1rAl2GB9w3gSbGIMuBJLYhc4KMQ+LgS8HYZFvjYAD5QwCcZ8IECPnGBT0Lg01rAm2GBzw3gIwV8lgEfKeA'\
    'zF3hhq/iTIQOdgR+1Vdy61sNdooAvMuATBTz7qb4IgS9rAe+GBb71cJep971FBnymXueYdfIPXyjqqlrWAn7YfkfXergrFPBGBnyhgDd'\
    'c4I0QeLMW8MOWlLnGw51ZKOBFLWZnbmjienXgpY2ua3l/dljvzzUe7p7f0KdAORnwhgLecYEXOndxLefODuvc+cbDnaGcOyNz7gzl3Bm'\
    'uc2ekfZRrOXd2WOfONx7uDGnmy5w7Q3r1XOfOCJ27uJZzZ4d17nzj4c5Qzp2ROXeGcu4M17kzUd3a3hd4N6xz51sPd5RzZ2TOnaGcO8N'\
    '17kxSVw93Bn5Y5863Hu6ENzT7fs36/syIKBOiTIgyIco0U5TpTA6iRp1FHWXKfRVv2C2L8JI8iqX8jhi/b2DFUoZI5KquXfTVq1BdqC5'\
    'UF6o7meo6pupao06BdlbdYfeLg2m8Z1Lbhla4iUBtG1ruJoK1+s5daCY0E5oJzZxMM7mHbqxTB+g7a+awUZvQ2IYjX0StbBuOfM+03G0'\
    '46/Vly9BMaCY0E5o5mWYGrmbqzx511sxhU4rBNTSTiq5Y2Ua2paIrlruRbaO+ZRuaCc2EZkIzJ9PMyNXMpD622Vkzhw14h0bqz1LhLys'\
    '7xGWp8JflHuKyWV+vDs2EZkIzoZmTaWbiamZRn3jvrJnDno0JoaGZ1MFnJzsGaamDz457DNKJM0AZmgnNhGZCM2fVTObU/weOVQ4L6ay'\
    'Zwx4rDI1DRpbKADlZBshSGSDHzQA5cQaoQDOhmdBMaOasmlm4munUc5Y6a+awJ7JDqmumozJATpYBclQGyHEzQE6aAXoyaAmaCc2EZkI'\
    'z59JMw61IckE9oq6vZvphh1mExkwDR2WAnCwD5KgMkONmgJw0A/RkRh00E5oJzYRmTqaZhquZST3ds7NmDjsHKJSGZlIZICfLADkqA+S'\
    '4GSAnbjHHJCFoJjQTmjmtZnInCbmiHozcWTOHnSQUG5OEHJUB8rIMkKMyQJ6bAfLiDmbMAYJmQjOhmdNqJncOkDfqmfKdNXPYOUCxMQf'\
    'IURkgL8sAOSoD5LkZIC/NAEXMAYJmQjOhmdNqJncOkHfqOo7OmjnsHKDYmAPkqQyQl2WAPJUB8twMkBdngDAHCJoJzYRmTquZ3DlAXt9'\
    'k1Fkzh50DFBtzgDyVAfKyDJCnMkCemwHy4gwQ5gBBM6GZ0MxpNZM7B8gndQlcZ80cdg5QbMwB8lQGyMsyQJ7KAHluBsiLM0CYAwTNhGZ'\
    'CM6fVTO4cIF/U/ZmdNXPYOUCxMQdI+hrJfUsMi74/s0DxoHhQPCjeXIrHnUgQjL4EEdQJ6gR1gjrnok7LPWQXXtCFB+oEdYI6QZ2TUSc'\
    '3Nx6cvhIN1AnqBHWCOiejTm4UKnh9MxaoE9QJ6gR1Tkad3N29EPQFSaBOUCeoE9Q5GXWyt4mivicH1AnqBHWCOueiTsfeJkr6uhRQJ6g'\
    'T1AnqnIw62dtEWd+aAeoEdYI6QZ2TUSd7m6joyxNAnaBOUCeoczLq5G4TxUU/Qx/UCeoEdYI6J6NO7jZRNPpR6qBOUCeoE9Q5F3V67jZ'\
    'RfMFEbVAnqBPUCeqcjDq520TR6QcrgzpBnaBOUOdk1MndJopeP18X1AnqBHWCOiejTvY2UdCPWQV1gjpBnaDOyaiTvU0UZWNWH8d1JtN'\
    '3zGoedcxqblRgGao2MsrmsBqqNjJyB7VG4Uz6x2GDvYEvwwLf6HGJkQI+i4A/vZ6lrlcHPguB9ysBfz9KeFDgG2UEkSpXj7IygkiVq0d'\
    'uGUEUTtR+HPTUG3gzLPCNidrPb+gToNIiAz4TwJ9erwp8WoTAx7WAt8MCHxvAUxqfjAx4SuOT4QIv7AR/HLLRG/hhO8FzqgP//IY+Bcq'\
    'KgH9+QxPXqwNvhcDntYAfttg25wbwVLFtkpXBJ6rYNnHL4JOw0fjxgHNv4IdtZ8ylAbylgPcy4C0FvOcC74V1KctawA9bMVaWBvBULWe'\
    'SVVknqpYzcausk7SP1awF/LA9OcU0gPcU8FEGvKeAj1zghc5dXMu5C8M6d6Xh3CWqVDDJnLtElQomrnOXpG2Sazl3YVjnrjScu0Q5d0n'\
    'm3CXKuUtc5y4Jnbu4lnMXh3XuSsO5S5Rzl2TOXaKcu8R17lLRdq73Bn5Y5640nLtEOXdZ5twlyrnLXOcuL9ri4N7AD+vclYZzlyjnLsu'\
    'cu0Q5d5nr3GWjbb/sDfywzl1pOHfCG5p/v1p1+2WyCCIhiIQgEoJIUwWRYmQGkbJTt1+COkGdoE5Q52zUyY2/Z69uvwR1gjpBnaDO2ag'\
    'zc6kzqNsvQZ2gTlAnqHM26uSeHMpR3X4J6gR1gjpBnZNR57kDHuepM6nbL0GdoE5QJ6hzNurkzubMWd1+CeoEdYI6QZ2zUaflUmdRt1+'\
    'COkGdoE5Q52zUyR1rXBZ1+yWoE9QJ6gR1zkadnkudRt1+CeoEdYI6QZ2zUSd3Inyx6vZLUCeoE9QJ6pyNOrmniYpTt1+COkGdoE5Q52z'\
    'UyT1NVLy6/RLUCeoEdYI6Z6NO7mmiEtTtl6BOUCeoE9Q5G3VyTxOVqG6/BHWCOkGdoM7JqDNzTxOVpG6/BHWCOkGdoM7ZqPPsaaJ/Hy9'\
    '32F4df95Pl3fb2/3u+HMuNr8eSe6BG4/f5VOxKblUQvafP/8fzvm0NA=='

def rom_size(template_name: str) -> int:
    name = template_name.split('/')[-1].split('\\')[-1]
    if name[:4] != 'ROM-':
        print('Template name must begin with "ROM-" followed by an integer number of bits.')
        exit(1)
    s = name[4:]
    a = 0
    for c in s:
        if c in [str(i) for i in range(10)]:
            a = a * 10 + int(c)
    return a

def generate_bp(program: list[int]) -> str:
    length = rom_bp_capacity
    while len(program) < length:
        program.append(0)

    b64_string = rom_bp_string[1:]
    bin_string = base64.b64decode(bytes(b64_string, 'utf-8'))

    json = zlib.decompress(bin_string)
    t = str(json)[2:-1]

    for i in range(length):
        t = t.replace(rom_bp_placeholder, str(program[i]), 1)

    z = zlib.compress(bytes(t, 'utf-8'), level=9)
    b = '0' + str(base64.b64encode(z))[2:-1]

    return b


## Opcodes
opcodes = {
    'NOOP': [0],
    'RESET': [2], 
    'MOV': [3, 4], 
    'MOVS': [5, 6],
    'STR': [7, 8], 
    'LDR': [9, 10],
    'LDRS': [11, 12],
    'ADD': [15, 20], 
    'MUL': [16, 21], 
    'AND': [17, 22], 
    'ORR': [18, 23], 
    'XOR': [19, 24], 
    'SUB': [25, 31, 37], 
    'DIV': [26, 32, 38], 
    'MOD': [27, 33, 39], 
    'EXP': [28, 34, 40], 
    'LSH': [29, 35, 41], 
    'RSH': [30, 36, 42], 
    'NOT': [43, 44], 
    'NOTS': [45, 46],
    'ADDS': [47, 52],
    'MULS': [48, 53],
    'ANDS': [49, 54],
    'ORRS': [50, 55],
    'XORS': [51, 56],
    'SUBS': [57, 63, 69], 
    'DIVS': [58, 64, 70], 
    'MODS': [59, 65, 71], 
    'EXPS': [60, 66, 72], 
    'LSHS': [61, 67, 73], 
    'RSHS': [62, 68, 74],
        'JMP': [75, 76],
        'JEQ': [77, 87], 
        'JNE': [78, 88], 
        'JLT': [79, 89], 
        'JGT': [80, 90], 
        'JLE': [81, 91], 
        'JGE': [82, 92], 
        'JNG': [83, 93], 
        'JPZ': [84, 94], 
        'JVS': [85, 95], 
        'JVC': [86, 96], 
        'PUSH': [97, 98],
    'POP': [99], 
    'POPS': [100], 
    'CLSP': [101]
}

builtin_macros = [
    'HALT',
    'CMP',
    'INC',
    'INCS',
    'DEC',
    'DECS',
    'CALL',
    'RETURN'
]

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
    'R12': 12,
    'SP': 13,
    'LR': 14,
    'PC': 15,
    'NIL': 255
}

debug = 1
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

def lexical_error(msg: str, i: int):
    print(f'Unknown token on line {i}: {msg}')
    global errors; errors += 1
    
def instr_to_machine_code(c: list, i: int) -> list:
    if len(opcodes[c[0]]) == 1:
        c = opcodes[c[0]][0] << 24
        return c
    
    if len(opcodes[c[0]]) > 1:
        
        # Comments show byte order of operands, for IMM16 the blank byte immediately to the back or front (when the last byte is not blank)
        #   is the LSB or MSB respectively
        # RN is the first register operand
        # RM is the second register operand
        # RD is the destination register, and synonymous with RN where RN is ommitted
        # IMM8 and IMM16 are immediate values of 8 and 16 bits respectively
        
        # OP RD RN _
        # OP RD IMM16 _
        if c[0] in ['MOV', 'MOVS', 'LDR', 'LDRS', 'NOT', 'NOTS']:
            # RN = RD
            if c[0] in ['NOT', 'NOTS'] and len(c) < 3:
                c.insert(1, c[1])
            
            # c = [OP, RD, RN, RM/IMM16]
            
            if len(c) < 3:
                syntax_error(f'too few arguments', code_info[i])
                return c
            elif len(c) > 3:
                syntax_error(f'too many arguments', code_info[i])
                return c
            
            if type(c[1]) != int:
                syntax_error('expected register as first argument', code_info[i])
                return c
            
            if type(c[2]) == int:
                t = 0
            else:
                t = 1
                c[2] = int(c[2][1:])
                if c[2] < -32768 or c[2] > 32767:
                    syntax_error(f'literal "#{c[2]}" out of range [-32768, 32767]', code_info[i])
                    return c
            
            c[0] = opcodes[c[0]][t]
            
            c = c[0] << 24 | c[1] << 16 | (c[2] << 8 if t == 0 else c[2] & 0xFFFF)
            return c
        
        # OP _ RM RN
        # OP _ IMM16 RN
        if c[0] in ['STR']:
            # c = [OP, RN, RM/IMM16]
            
            if len(c) < 3:
                syntax_error(f'too few arguments', code_info[i])
                return c
            elif len(c) > 3:
                syntax_error(f'too many arguments', code_info[i])
                return c
            
            if type(c[1]) != int:
                syntax_error('expected register as first argument', code_info[i])
                return c
            
            if type(c[2]) == int:
                t = 0
            else:
                t = 1
                c[2] = int(c[2][1:])
                if c[2] < -32768 or c[2] > 32767:
                    syntax_error(f'literal "#{c[2]}" out of range [-32768, 32767]', code_info[i])
                    return c
            
            c[0] = opcodes[c[0]][t]
            
            c = c[0] << 24 | c[1] | (c[2] << 8 if t == 0 else (c[2] & 0xFFFF) << 8)
            return c
        
        # OP RD RN RM
        # OP RD RN IMM8
        if c[0] in ['ADD', 'MUL', 'AND', 'ORR', 'XOR', 'ADDS', 'MULS', 'ANDS', 'ORRS', 'XORS']:
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
                syntax_error('expected register as first argument', code_info[i])
                return c
            if type(c[2]) != int:
                syntax_error('expected register as second argument', code_info[i])
                return c
            
            if type(c[3]) == int:
                t = 0
            else:
                t = 1
                c[3] = int(c[3][1:])
                if c[3] < -128 or c[3] > 127:
                    syntax_error(f'literal "#{c[2]}" out of range [-128, 127]', code_info[i])
                    return c
            
            c[0] = opcodes[c[0]][t]
            
            c = c[0] << 24 | c[1] << 16 | c[2] << 8 | c[3] & 0xFF
            return c
        
        # OP RD RN RM
        # OP RD RN IMM8
        # OP RD IMM8 RM
        if c[0] in ['SUB', 'DIV', 'MOD', 'EXP', 'LSH', 'RSH', 'SUBS', 'DIVS', 'MODS', 'EXPS', 'LSHS', 'RSHS']:
            # RN = RD
            if len(c) < 4:
                c.insert(1, c[1])
            
            # c = [OP, RD, RN, RM/IMM8] xor [OP, RD, IMM8, RM]
            
            if len(c) < 4:
                syntax_error(f'too few arguments', code_info[i])
                return c
            elif len(c) > 4:
                syntax_error(f'too many arguments', code_info[i])
                return c
            
            if type(c[1]) != int:
                syntax_error('expected register as first argument', code_info[i])
                return c
            if type(c[2]) != int and type(c[3]) != int:
                syntax_error('expected register as second or third argument', code_info[i])
                return c
            
            if type(c[2]) == int and type[c[3]] == int:
                t = 0
            elif type(c[2]) != int:
                t = 2
                c[2] = int(c[2][1:])
                if c[2] < -128 or c[2] > 127:
                    syntax_error(f'literal "#{c[2]}" out of range [-128, 127]', code_info[i])
                    return c
            elif type(c[3]) != int:
                t = 1
                c[3] = int(c[3][1:])
                if c[3] < -128 or c[3] > 127:
                    syntax_error(f'literal "#{c[2]}" out of range [-128, 127]', code_info[i])
                    return c
            
            c[0] = opcodes[c[0]][t]
            
            c = c[0] << 24 | c[1] << 16 | (c[2] & 0xFF) << 8 | c[3] & 0xFF
            return c

        # OP _ RN _
        # OP _ IMM16 _
        if c[0] in ['JMP', 'JEQ', 'JNE', 'JLT', 'JGT', 'JLE', 'JGE', 'JNG', 'JPZ', 'JVS', 'JVC', 'PUSH']:
            # c = [OP, RN/IMM16]
            
            if len(c) < 2:
                syntax_error(f'too few arguments', code_info[i])
                return c
            elif len(c) > 2:
                syntax_error(f'too many arguments', code_info[i])
                return c
            
            if type(c[1]) == int:
                ot = 0
                if c[0] == 'PUSH':
                    t = 0
                else:
                    t = 1
            else:
                ot = 1
                if c[0] == 'PUSH':
                    t = 1
                else:
                    t = 0
                c[1] = int(c[1][1:])
                if c[1] < -32768 or c[1] > 32767:
                    syntax_error(f'literal "#{c[1]}" out of range [-32768, 32767]', code_info[i])
                    return c
            
            c[0] = opcodes[c[0]][t]
            
            c = c[0] << 24 | (c[1] << 8 if ot == 0 else c[1] & 0xFFFF)
            return c
    
    return c

def macro_to_instr(c: list):
    o = c[0]
    out = []
    
    if o == 'HALT':
        out.append(['JMP', 'PC'])
    elif o == 'CMP':
        out.append(c)
        out[-1][0] = 'SUBS'
    elif o == 'INC':
        out.append(['ADD', c[1], c[1], '#1'])
    elif o == 'INCS':
        out.append(['ADDS', c[1], c[1], '#1'])
    elif o == 'DEC':
        out.append(['SUB', c[1], c[1], '#1'])
    elif o == 'DECS':
        out.append(['SUBS', c[1], c[1], '#1'])
    elif o == 'CALL':
        out.append(['ADD', 'LR', 'PC', '#2'])
        out.append(['JMP', c[1]])
    elif o == 'RETURN':
        out.append(['JMP', 'LR'])
    
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
            
        # Everything not picked up is a lexical error
        else:
            lexical_error(c[0], lineinfo[i])
    
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
        machine_code[i] = instr_to_machine_code(instr, i)
    
    if debug:
        print('## SECOND PASS ##')
        for c in machine_code:
            print(c)
        print('## END SECOND PASS ##')
    
    ## Output
    if errors:
        print(f'{errors} error{"s" if errors > 1 else ""} detected')
        exit(0)
    
    ## Third pass
    bp = generate_bp(machine_code)
    
    if len(sys.argv) == 3:
        with open(sys.argv[2], 'w') as fd:
            fd.write(bp)
    else:
        print(bp)