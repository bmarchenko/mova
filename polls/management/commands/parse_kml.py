from polls.models import Place, Region, Map
import os
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
import re
module_dir = os.path.dirname(__file__)  # get current directory



def parse_kml(stderr, tag_file):

    with file(os.path.join(module_dir, tag_file), "rU") as kml_file:
        handler = kml_file.read()
        soup = BeautifulSoup(handler)
        for message in soup.findAll('placemark'):
            coordinates = message.find('coordinates').text.split(',')
            name = html_decode(message.find('name').text)
            description = html_decode(message.find('description').text).replace('"', "'")
            style = message.find('styleurl').text.strip('#')
            #import ipdb; ipdb.set_trace()

            marker = soup.find(attrs={'id': re.compile(r".*\b{0}\b.*".format(style))}).find('href').text
            if marker == u'http://maps.gstatic.com/mapfiles/ms2/micons/green.png':
                color = 3
            elif marker == u'http://maps.gstatic.com/mapfiles/ms2/micons/yellow.png':
                color = 2
            else:
                color = 1

            Place(title=name, address=description, color=color, map_geo=Map.objects.all()[0], region=Region.objects.all()[0], geometry="POINT({0} {1})".format(coordinates[0], coordinates[1])).save()

            print style

        #try:
        #    data = csv.reader(tag_file, delimiter=",", quotechar='\"')
        #except Exception as e:
        #    raise CommandError("wrong file format")
        #file_fields = data.next()
        #init_disciplines = Discipline.objects.all().count()
        #init_strands = Strand.objects.all().count()
        #init_grades = Grade.objects.all().count()
        #init_focuses = Focus.objects.all().count()
        #init_tags = AlignmentTag.objects.all().count()
        #print "Initially {0} disciplines, {1} strands {2} grades {3} focuses {4} tags".format(init_disciplines, init_strands, init_grades, init_focuses, init_tags)
        ##restructure field values
        #errors = []
        #for row in data:
        #    try:
        #        fields_values = dict(zip(file_fields, row))
        #        # import pdb; pdb.set_trace()
        #        if "Grade" in fields_values["Discipline"] or "Grade" in fields_values["Grade"]:
        #            continue
        #        discipline, created = Discipline.objects.get_or_create(name=fields_values["Discipline"])
        #        if created:
        #            print "created {0}".format(discipline)
        #        strand, created = Strand.objects.get_or_create(name=fields_values["Strand"], discipline=discipline)
        #        if created:
        #            print "created {0}".format(strand)
        #
        #        grade, created = Grade.objects.get_or_create(name=fields_values["Grade"])
        #        if created:
        #            print "created {0}".format(grade)
        #        #find focus, they put numbers on the beginning of string. They should be ignored as well as space after numbers.
        #        try:
        #            int(fields_values["Focus"][1])
        #            focus_name = fields_values["Focus"][3:]
        #        except ValueError:
        #            focus_name = fields_values["Focus"][2:]
        #        focus, created = Focus.objects.get_or_create(name=focus_name, strand=strand, grade=grade)
        #        if created:
        #            print "created {0}".format(focus)
        #        key_performance = True if fields_values["Key Performance Standard 1=yes"] == "1" else False
        #        description=fields_values["Text"].replace("\xd0", "-").replace("\xd5", "'").replace("\xd4", "'").replace("\xc9", "")
        #        full_code = fields_values["ID"]
        #        tag, created = AlignmentTag.objects.get_or_create(key_performance=key_performance, description=description, full_code=full_code, focus=focus)
        #        if created:
        #            print "created {0}".format(tag)
        #    except IntegrityError:
        #        errors.append("line: {0}, tagcode: {1} tag exists with description: '{2}', description from file: '{3}'".format(data.line_num, full_code, AlignmentTag.objects.get(full_code=full_code).description, description))
        #    except Exception as e:
        #        import pdb; pdb.set_trace()
        #final_disciplines = Discipline.objects.all().count()
        #final_strands = Strand.objects.all().count()
        #final_grades = Grade.objects.all().count()
        #final_focuses = Focus.objects.all().count()
        #final_tags = AlignmentTag.objects.all().count()
        #print "Created {0} disciplines, {1} strands {2} grades {3} focuses {4} tags".format(final_disciplines-init_disciplines, final_strands-init_strands, final_grades-init_grades, final_focuses-init_focuses, final_tags-init_tags)
        #print "errors:"
        #print errors
def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--file', '-f', dest='file',
                    help='File path, from the current folder.'),
    )
    help = 'Creates SEC Aligment tags from file if not exist.'

    requires_model_validation = False
    can_import_settings = False

    def handle(self, **options):
        file = options.get('file')
        parse_kml(self.stderr, tag_file=file)


