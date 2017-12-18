import imaplib
import email

FROM_EMAIL = "<seuemail>@gmail.com"  # substitua <seuemail> pelo seu email.
FROM_PWD = "<suasenha>"  # substitua <suasenha> pela sua senha
SMTP_SERVER = "imap.gmail.com"  # padrão
SMTP_PORT = 993  # padrão


def read_email():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox', readonly=False)

        type_mail, data = mail.search(None, 'SUBJECT ASSUNTO-ESPECÍFICO')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print("Reading emails from {} to {}.\n\n".format(latest_email_id, first_email_id))

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(str.encode(str(i)), '(RFC822)')

            for response_part in data:
                if not isinstance(response_part, tuple):
                    continue

                msg = email.message_from_string(response_part[1].decode('utf-8'))
                mail_str = str(msg)

                # Se e-mail não contém a estrutura que precisamos, não processa
                if mail_str.find('<td class="luceeH0">SQL</td>') <= 1:
                    continue

                email_subject = msg['subject']
                email_from = msg['from']

                # INFORMAÇÃO DE DETALHE
                detail_pos_ini = mail_str.find('class="luceeH0">Detail</td>')
                detail_pos_inter = mail_str.find('<td class="luceeN1">', detail_pos_ini)
                detail_pos_fim = mail_str.find('</td>', detail_pos_inter)
                detail_str = mail_str[detail_pos_inter + 20:detail_pos_fim]

                # SQL EVENTO
                sql_pos_ini = mail_str.find('<td class="luceeH0">SQL</td>')
                sql_pos_inter = mail_str.find('<td class="luceeN1">', sql_pos_ini)
                sql_pos_fim = mail_str.find('</td>', sql_pos_inter)
                sql_str = mail_str[sql_pos_inter + 20:sql_pos_fim]

                # DATA/HORA EVENTO
                datetime_error_pos_ini = mail_str.find('<h2>{ts ')
                datetime_error_pos_fim = mail_str.find('</h2>', datetime_error_pos_ini)
                datetime_error = mail_str[datetime_error_pos_ini + 4:datetime_error_pos_fim]

                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')
                print('DATA/HORA: ' + datetime_error + '\n')
                print('EVENTO: ' + detail_str.replace('\n', ' ') + '\n')
                print('SQL: \n' + sql_str + '\n')

                mail.store(str.encode(str(i)), '+X-GM-LABELS', 'seu_label')

                print('----------------------------------------------------------')
                print('----------------------------------------------------------')

        mail.logout()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    read_email()
