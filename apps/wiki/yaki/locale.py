#!/usr/bin/env python
# encoding: utf-8
'''
Locale.py

Localizable strings

This module will hold all localizable strings in the Yaki codebase, _except_ those in HTML and theme files

Created by Rui Carmo on 2007-08-25.
Published under the MIT license.
'''

i18n = {
  'en_US': {
    'uri_schemas': {
      '*':{'title': u'unknown protocol linking to %(uri)s','class': u'generic'},
      'http':{'title': u'external link to %(uri)s','class': u'http'},
      'https':{'title': u'secure link to %(uri)s','class': u'https'},
      'ftp':{'title': u'file transfer link to %(uri)s','class': u'ftp'},
      'gopher':{'title': u'(probably deprecated) link to %(uri)s','class': u'ftp'},
      'sftp':{'title': u'secure file transfer link to %(uri)s','class': u'ftp'},
      'ssh':{'title': u'secure shell session to %(uri)s','class': u'terminal'},
      'telnet':{'title': u'(probably insecure) terminal session to %(uri)s','class': u'terminal'},
      'mailto':{'title': u'e-mail to %(uri)s','class': u'mail'},
      'outlook':{'title': u'MAPI link to %(uri)s','class': u'mail'},
      'skype':{'title': u'call %(uri)s using Skype','class': u'call'},
      'sip':{'title': u'call %(uri)s using SIP','class': u'call'},
      'tel':{'title': u'call %(uri)s using SIP','class': u'call'},
      'callto':{'title': u'call %(uri)s','class': u'call'}
    },
    # page components
    'pagetrail': u'Page Trail',
    'seealso': u'See Also',
    'indexing_message': u'Indexing in progress, cross-references will be refreshed soon.',
    # link descriptions
    'external_link_format': u'external link to %s',
    'permalink_description': u'permanent link to this entry',
    'link_anchor_format': u'link to %s in this page',
    'link_defined_notindexed_format': u'%s is defined, but has not been indexed yet.',
    'link_interwiki_format': u'link to %s on another Wiki',
    'link_undefined_format': u'%s is not defined yet',
    'link_update_format': u'%s was updated %s ago',
    'created_on_format': u'Created on %s by %s',
    # Plugins
    'journal_date_format': u'%(weekday)s, %(mday)s %(month)s %(year)s',
    'updated_ago_format': u'updated %s ago',
    'not_updated': u'not updated since',
    'some_time': u'some time',
    'less_1min': u'less than one minute',
    'no_search': u'No search performed',
    'no_results': u'No results found for',
    'search_disabled': u'Content has not been indexed yet, search is temporarily disabled.',
    'search_results': u'Search results for',
    # Words
    'Page': u'Page',
    'Created': u'Created',
    'Modified': u'Modified',
    # Time
    'day': u'day',
    'days': u'days',
    'week': u'week',
    'weeks': u'weeks',
    'year': u'year',
    'years': u'years',
    'month': u'month',
    'months': u'months',
    'hour': u'hour',
    'hours': u'hours',
    'minute': u'minute',
    'minutes': u'minutes',
    'second': u'second',
    'seconds': u'seconds',
    # Short month names
    'Jan': u'Jan',
    'Feb': u'Feb',
    'Mar': u'Mar',
    'Apr': u'Apr',
    'May': u'May',
    'Jun': u'Jun',
    'Jul': u'Jul',
    'Aug': u'Aug',
    'Sep': u'Sep',
    'Oct': u'Oct',
    'Nov': u'Nov',
    'Dec': u'Dec',
    # Months
    'January': u'January',
    'February': u'February',
    'March': u'March',
    'April': u'April',
    'May': u'May',
    'June': u'June',
    'July': u'July',
    'August': u'August',
    'September': u'September',
    'October': u'October',
    'November': u'November',
    'December': u'December',
    # Weekdays
    'Monday': u'Monday',
    'Tuesday': u'Tuesday',
    'Wednesday': u'Wednesday',
    'Thursday': u'Thursday',
    'Friday': u'Friday',
    'Saturday': u'Saturday',
    'Sunday': u'Sunday'
  },
  'pt_PT': {
    'uri_schemas': {
      '*':{'title': u'link de protocolo desconhecido para %(uri)s','class': u'generic'},
      'http':{'title': u'link externo para %(uri)s','class': u'http'},
      'https':{'title': u'link seguro para %(uri)s','class': u'https'},
      'ftp':{'title': u'link FTP para %(uri)s','class': u'ftp'},
      'gopher':{'title': u'link gopher (provavelmente desactualizado) para %(uri)s','class': u'ftp'},
      'sftp':{'title': u'link SFTP para %(uri)s','class': u'ftp'},
      'ssh':{'title': u'link SSH para %(uri)s','class': u'terminal'},
      'telnet':{'title': u'link telnet (provavelmente inseguro) para %(uri)s','class': u'terminal'},
      'mailto':{'title': u'e-mail para %(uri)s','class': u'mail'},
      'outlook':{'title': u'link MAPI para %(uri)s','class': u'mail'},
      'skype':{'title': u'ligar para %(uri)s via Skype','class': u'call'},
      'sip':{'title': u'ligar para %(uri)s via SIP','class': u'call'},
      'tel':{'title': u'ligar para %(uri)s via SIP','class': u'call'},
      'callto':{'title': u'ligar para %(uri)s','class': u'call'}
    },
    # page components
    'pagetrail': u'Migalhas',
    'indexing_message': u'Indexação em curso, as referências serão actualizadas dentro de momentos.',
    'seealso': u'Ver também',
    # link descriptions
    'external_link_format': u'link externo para %s',
    'permalink_description': u'link permanente para esta entrada',
    'link_anchor_format': u'link para %s nesta página',
    'link_defined_notindexed_format': u'%s existe, mas não foi ainda indexado.',
    'link_interwiki_format': u'link para %s noutro Wiki',
    'link_undefined_format': u'%s ainda não existe',
    'link_update_format': u'%s foi actualizada há %s',
    'created_on_format': u'Criada em %s por %s',
    # Plugins
    'journal_date_format': u'%(weekday)s, %(mday)s de %(month)s de %(year)s',
    'updated_ago_format': u'actualizada há %s',
    'not_updated': u'sem actualizações',
    'some_time': u'algum tempo',
    'less_1min': u'menos de um minuto',
    'no_search': u'Não foi realizada qualquer pesquisa',
    'no_results': u'Não foram encontrados resultados para',
    'search_disabled': u'O conteúdo do site ainda não foi indexado, a pesquisa está temporariamente desactivada.',
    'search_results': u'Resultados da pesquisa por',
    # Words
    'Page': u'Página',
    'Created': u'Criação',
    'Modified': u'Actualizações',
    # time
    'day': u'dia',
    'days': u'dias',
    'week': u'semana',
    'weeks': u'semanas',
    'month': u'mês',
    'months': u'meses',
    'year': u'ano',
    'years': u'anos',
    'hour': u'hora',
    'hours': u'horas',
    'minute': u'minuto',
    'minutes': u'minutos',
    'second': u'segundo',
    'seconds': u'segundos',
    # Short month names
    'Jan': u'Jan',
    'Feb': u'Fev',
    'Mar': u'Mar',
    'Apr': u'Abr',
    'May': u'Mai',
    'Jun': u'Jun',
    'Jul': u'Jul',
    'Aug': u'Ago',
    'Sep': u'Set',
    'Oct': u'Out',
    'Nov': u'Nov',
    'Dec': u'Dez',
    # Months
    'January': u'Janeiro',
    'February': u'Fevereiro',
    'March': u'Março',
    'April': u'Abril',
    'May': u'Maio',
    'June': u'Junho',
    'July': u'Julho',
    'August': u'Agosto',
    'September': u'Setembro',
    'October': u'Outubro',
    'November': u'Novembro',
    'December': u'Dezembro',
    # Weekdays
    'Monday': u'Segunda-Feira',
    'Tuesday': u'Terça-Feira',
    'Wednesday': u'Quarta-Feira',
    'Thursday': u'Quinta-Feira',
    'Friday': u'Sexta-Feira',
    'Saturday': u'Sábado',
    'Sunday': u'Domingo'
  }
}