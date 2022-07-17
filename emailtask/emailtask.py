import csv
from contextlib import contextmanager
import argparse


@contextmanager
def open_file(name):
    f = open(name, 'r')
    try:
        yield f
    finally:
        f.close()


class EmailCollector():
    def __init__(self):
        self.all_email = []
        self.correct_email_list = []
        self.open_files_read_email()
        self.clear_files_from_whitespace()
        self.validate_email()

    def open_files_read_email(self):
        # skrocic sciezke. Niepotrzebne powtorzenia
        prefixPath = 'recruitment-task-backend-internship-main/emails'

        with open_file(prefixPath + '/email-pack-1.txt') as email_pack_1, \
                open_file(prefixPath + '/emails-pack-2.txt') as email_pack_2, \
                open_file(prefixPath + '/emails3.txt') as email_pack_3, \
                open_file(prefixPath + '/other-emails4.txt') as email_pack_4, \
                open_file(prefixPath + '/last-email-pack.csv') as email_pack_5_CSV:

            email_pack_list = [email_pack_1,
                               email_pack_2,
                               self.clear_email_from_csv_file(email_pack_5_CSV),
                               email_pack_4,
                               email_pack_3,
                               ]

            for email_pack in email_pack_list:
                for email in email_pack:
                    self.all_email.append(email)

    def clear_files_from_whitespace(self):
        raw_data_list = []
        for line in self.all_email:
            line = line.strip('\n')
            raw_data_list.append(line)
        self.all_email = raw_data_list

    def clear_email_from_csv_file(self, csv_file):
        reader = csv.reader(csv_file, delimiter=';')
        temporary_raw_data_list = []
        header = 'email'
        for row in reader:
            if row[1] == header:
                continue
            temporary_raw_data_list.append(row[1])

        return temporary_raw_data_list

    def validate_email(self):
        incorrect_email_list = []
        for email in self.all_email:
            if email.count('@') != 1 \
                    or email.find('@') < 1 \
                    or email.find('@.') > -1 \
                    or email.find('.@') > -1 \
                    or email.rfind('.') < 1 \
                    or email.rfind('.') > 4 \
                    and email[email.rfind('.'):].isalnum():
                incorrect_email_list.append(email)
            else:
                self.correct_email_list.append(email)

        return incorrect_email_list

    def search_value(self, phrase):
        is_pharse_in_email_list = []
        for email in self.all_email:
            if phrase in email:
                is_pharse_in_email_list.append(email)

        return is_pharse_in_email_list

    def sort_alphabetical_by_domain(self):
        domain_dict = {}
        for email in self.correct_email_list:
            domain = email.split('@')[1]

            if domain in domain_dict:
                domain_dict[domain].append(email)
            else:
                domain_dict[domain] = [email]

        for item, value in sorted(domain_dict.items()):
            ListToStr = '\n\t'.join(map(str, sorted(value)))

            print(f'Domain {item} ({len(value)}):\n\t{ListToStr}')

    def clear_data_logsfile_to_obtain_email(self, raw_data_from_file):
        logs_email_list = []
        for line in raw_data_from_file:
            email = line.split('\'')
            logs_email_list.append(email[1])

        return logs_email_list

    def is_exist_logsemail_in_all_email(self, path_to_file):
        data_from_logs_file = []
        with open_file(path_to_file) as email_pack_6_logs:
            # 6-logs? co to robi
            for logs_email in email_pack_6_logs:
                data_from_logs_file.append(logs_email)

        message_not_send_to_email_list = []
        logs_email = self.clear_data_logsfile_to_obtain_email(data_from_logs_file)
        for email in self.correct_email_list:
            if email not in logs_email:
                message_not_send_to_email_list.append(email)

        return sorted(message_not_send_to_email_list)


def create_commad():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-ir", "--incorrect-emails", action="store_true")
    group.add_argument("-s", "--search", type=str, )
    group.add_argument("-gbd", "--group-by-domain", action="store_true")
    group.add_argument("-feil", "--find-email-not-in-logs", type=str, help='path-to-logs-in')
    return parser.parse_args()


def main():
    email_collector = EmailCollector()

    command = create_commad()

    if command.incorrect_emails:
        print('Invalid emails (10):')
        for email in email_collector.validate_email():
            print('\t', email)
    elif command.group_by_domain:
        print(email_collector.sort_alphabetical_by_domain())
    elif command.search:
        print('Found emails with ', '\'' + command.search +
              '\'', ' in email (' + str(len(email_collector.search_value(command.search))) + '):')
        for email in email_collector.search_value(command.search):
            print('\t', email)
    elif command.find_email_not_in_logs:

        print('Email not sent:(' + str(len(email_collector.is_exist_logsemail_in_all_email(
            command.find_email_not_in_logs))) + ')')
        for email in email_collector.is_exist_logsemail_in_all_email(command.find_email_not_in_logs):
            print('\t', email)


main()
