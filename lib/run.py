#!/usr/bin/env python3
import argparse
import sys
import yaml
import ntpath

from nxapi.ldap import Ldap
from nxapi.blob import Blob
from nxapi.repo import Repo
from nxapi.user import User
from nxapi.role import Role
from nxapi.nexussession import NexusSession


def create_parser():
    parser = argparse.ArgumentParser(
        prog=None,
        usage=None,
        description=None,
        epilog=None,
        parents=[],
        prefix_chars='-',
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler='error',
        add_help=True,
        allow_abbrev=True
    )

    parser.add_argument(
        '-n', '--nexus',
        type=str,
        default='http://nuc.local:8083',
        help='Sonatype Nexus3 URL'
    )

    parser.add_argument(
        '-u', '--user',
        type=str,
        default='admin',
        help='Nexus3 admin user'
    )

    parser.add_argument(
        '-p', '--passwd',
        type=str,
        default='admin123',
        help='Nexus3 admin password'
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        default='examples/projects/project1_meta.yaml',
        help='project model yaml'
    )

    return parser


def yaml_read(path):
    """
    Простая функция чтения yaml файла
    :param path: path to yaml file
    :return: project map dictionary
    """
    with open(path, 'r') as project_model:
        try:
            model = yaml.safe_load(project_model)
        except yaml.YAMLError as exc:
            print(exc)

        return model


def create_user_local(session, project_map):
    """
    Создание локальных пользователей Nexus
    :param session: an opened session of NexusSession
    :param project_map: project map dictionary
    :return: list of users for create
    """
    nexus_users_dict = User(session).list()
    project_users_for_create = []
    # подготовка списка пользователей для создания
    for role in project_map['TEAM']['ROLES']:
        users_in_role = project_map['TEAM']['ROLES'][role]
        for user in users_in_role:
            if user not in project_users_for_create:
                project_users_for_create.append(user)

    # создание пользователей, если отсутствуют
    for user in project_users_for_create:
        if user not in nexus_users_dict:
            User(session).create(**{'userId': user})

    return project_users_for_create


def delete_user_local(session, project_users_for_create):
    """
    Удаление локальных пользователей Nexus
    :param session: an opened session of NexusSession
    :param project_users_for_create: list of users for create
    :return: list of users for delete
    """

    nexus_users_dict = User(session).list()
    # подготовка списка пользователей для удаления
    project_users_for_delete = []
    for user in nexus_users_dict:
        if user not in project_users_for_create and \
                user not in ['anonymous', 'admin']:
            project_users_for_delete.append(user)

    # удаление локальных пользователей из nexus, если не найдены в модели проекта
    for user in project_users_for_delete:
        User(session).delete(**{'userId': user})

    return project_users_for_delete


def create_blob(session, project_model_nexus):
    """
    Создание blob storages
    :param session: an opened session of NexusSession
    :param project_model_nexus: nexus part of project map dict
    """
    nexus_blob_dict = Blob(session).list()

    for bm in project_model_nexus['blob']:
        if bm['name'] in nexus_blob_dict:
            pass
            # TODO: опасная операция, может сменить путь до блоба
            # Blob(session).update(**bm)
        else:
            Blob(session).create(**bm)


def create_repository(session, project_model_nexus):
    """
    Создание репозиториев
    :param session: an opened session of NexusSession
    :param project_model_nexus: nexus part of project map dict
    """
    nexus_repo_dict = Repo(session).list()
    nexus_blob_dict = Blob(session).list()
    project_model_repository = project_model_nexus['repository']

    for repo in project_model_repository:
        if 'privilegesOnly' in repo and repo['privilegesOnly']:
            print(f'INFO {repo} not created, only privileges mode')
        else:
            if repo['name'] in nexus_repo_dict:
                Repo(session).update(**repo)  # TODO: нужна проверка дифа nexus/model
            else:
                if 'blobStoreName' not in repo and repo['name'] not in nexus_blob_dict:
                    # если не указано названия blob, то
                    # создать с именем репозитория в расположении по умолчанию
                    Blob(session).create(**repo)
                Repo(session).create(**repo)


def privilege_translation(map_privilege, role_privileges_dict, full_role_name, repo_name, repo_type):
    """
    Переводит простое описание привилегии из описания проекта
    в структуру привилегий для nexus
    :param map_privilege: (read/write/delete)
    :param role_privileges_dict: dict {read: [nx-repository-view-pr1-read, nx-repository-view-pr1-browse]}
    :param full_role_name rb-{project_name}-{role}
    :return: role privileges dict
    """

    translation_dict = {
        'read': ['read', 'browse'],
        'write': ['edit', 'add'],
        'delete': ['delete']
    }

    if map_privilege in translation_dict:
        for nexus_privilege in translation_dict[map_privilege]:
            full_privilege_name = f'nx-repository-view-{repo_type}-{repo_name}-{nexus_privilege}'
            if full_role_name not in role_privileges_dict:
                role_privileges_dict[full_role_name] = [full_privilege_name]
            else:
                role_privileges_dict[full_role_name].append(full_privilege_name)

    return role_privileges_dict


def create_role(session, project_name, project_model_nexus):
    """
    Создание локальных ролей Nexus
    :param session: an opened session of NexusSession
    :param project_name: name of project
    :param project_model_nexus: nexus part of project map dict
    """
    roles_dict = Role(session).list()
    privileges_for_role = {}

    for repo in project_model_nexus['repository']:
        repo_name = repo['name']
        repo_type = repo['repoType']
        if repo_type == 'maven':
            repo_type = 'maven2'

        for role in project_model_nexus['privileges']:
            full_role_name = f'rb-{project_name}-{role}'
            role_privileges = project_model_nexus['privileges'][role]
            for privilege in role_privileges:
                privileges_for_role = privilege_translation(privilege, privileges_for_role, full_role_name, repo_name,
                                                            repo_type)

    for role in privileges_for_role:
        # TODO: требуется добавить удаление ролей не из модели проекта
        if role in roles_dict:
            Role(session).update(
                name=role,
                privileges=privileges_for_role[role]
            )
        else:
            Role(session).create(
                name=role,
                privileges=privileges_for_role[role]
            )


def main():
    parser = create_parser()
    parser_namespace = parser.parse_args(sys.argv[1:])

    nexus_api_url = parser_namespace.nexus + '/service/rest'
    nexus_api_auth = (parser_namespace.user, parser_namespace.passwd)
    project_model_path = parser_namespace.file

    project_name = ntpath.basename(project_model_path).replace('_meta.yaml', '')

    with NexusSession(nexus_api_url, nexus_api_auth) as s:
        project_map = yaml_read(project_model_path)

        # Проверка защиты обработки модели
        if project_map['READY']:

            # Обработка ресурсов nexus
            if project_map['RESOURCES'] and project_map['RESOURCES']['nexus']:
                project_model_nexus = project_map['RESOURCES']['nexus']

                # Blob
                if 'blob' in project_model_nexus:
                    create_blob(s, project_model_nexus)

                # Repository
                if 'repository' in project_model_nexus:
                    create_repository(s, project_model_nexus)

                # Roles
                if 'privileges' in project_model_nexus:
                    create_role(s, project_name, project_model_nexus)

                # Работа с локальными пользователями
                # позволяет обрабатывать дополнение и удаление локальных пользователей
                # исключена обработка admin и anonymous
                if project_map['TEAM'] and \
                        project_map['TEAM']['USER_LOCATION'] == 'local':
                    project_users_for_create = create_user_local(s, project_map)
                    project_users_for_delete = delete_user_local(s, project_users_for_create)
                    # Добавление ролей для пользователей локальных
                    nexus_users_dict = User(s).list()
                    for role in project_map['TEAM']['ROLES']:
                        users_in_role = project_map['TEAM']['ROLES'][role]
                        for user in users_in_role:
                            if user in nexus_users_dict:
                                user_project_role = f'rb-{project_name}-{role}'
                                nexus_roles = nexus_users_dict[user]['roles']
                                if user_project_role not in nexus_roles:
                                    nexus_roles.append(user_project_role)
                                User(s).update(**{'userId': user, 'roles': nexus_roles, 'source': 'default'})


if __name__ == '__main__':
    main()
