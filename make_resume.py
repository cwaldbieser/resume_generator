#! /usr/bin/env python

import yaml
import sys
import os
import os.path
from textwrap import dedent, wrap
import string
import getopt

def run(file_name, outfile_name, **options):
    f = open(file_name, "r")
    data = yaml.load(f)
    f.close()
    junk, ext = os.path.splitext(outfile_name)
    if ext == '.tex':
        write_latex(data, outfile_name)
    elif ext == '.html':
        write_html(data, outfile_name, **options)
    elif ext == '.txt':
        write_text(data, outfile_name)
    else:
        print >> sys.stderr, "Unknown output format, '%s'." % ext
        sys.exit(1)

def write_text(data, outfile_name):
    WIDTH = 80
    INDENT = 20
    
    personal = data['personal']
    education = data['education']
    
    name = personal.get('name', '')
    address_line_1 = personal.get('address_line_1', '')
    address_line_2 = personal.get('address_line_2', '')
    phone = personal.get('phone', '')
    email = personal.get('email', '')
    objective = personal.get('objective', '')
    degree = personal.get('degree', '')
    field = personal.get('field', '')
    institution = personal.get('institution', '')
    institution_location = personal.get('institution_location', '')
    graduation_year = personal.get('graduation_year', '')
    computer_languages = personal.get('computer_languages', '')
    computer_platforms = personal.get('computer_platforms', '')
    
    fout = open(outfile_name, "w")
    print >> fout, name.center(WIDTH)
    print >> fout, ("=" * len(name)).center(WIDTH)
    print >> fout, ""
    print >> fout, address_line_1.center(WIDTH)
    print >> fout, address_line_2.center(WIDTH)
    print >> fout, phone.center(WIDTH)
    print >> fout, email.center(WIDTH)
    print >> fout, ""
    print >> fout, ""
    skills_lines = wrap("*Tools and Languages:*" + ', '.join(data['computer_skills']), WIDTH - INDENT)
    for i, line in enumerate(skills_lines):
        if i == 0:
            leading = "COMPUTER SKILLS".ljust(INDENT)
        else:
            leading = " " * INDENT
        print >> fout, leading + line
    
    platform_lines = wrap("*Platforms:*" + ', '.join(data['platforms']), WIDTH - INDENT)
    leading = " " * INDENT
    for line in platform_lines:
        print >> fout, leading  + line
    
    #Previous positions held.
    print >> fout, ""
    experience = data['experience']
    for position in experience:
        position_name = position.get('position', '')
        month = position.get('month', '')
        year = position.get('year', '')
        organization = position.get('organization', '')
        location = position.get('location', '')
        
        print >> fout, "EXPERIENCE:".ljust(INDENT) + position_name + (str(month) + " " + str(year)).rjust(WIDTH - INDENT - len(position_name))
        print >> fout, (" " * INDENT) + organization
        print >> fout, ""
        
        details = position['details']
        for detail in details:
            leading_size = INDENT + 2
            for i, line in enumerate(wrap(detail, WIDTH - leading_size)):
                if i == 0:
                    leading = (" " * (INDENT)) + "* "
                else:
                    leading = " " * leading_size
                print >> fout, leading + line
        print >> fout, ""

    references = data['references']
    for i, reference in enumerate(references):
        ref_name = reference.get('name', '')
        ref_phone = reference.get('phone', '')
        if i == 0:
            leading = "REFERENCES:".ljust(INDENT) + "* "
        else:
            leading = " " * (INDENT) + "* "
        print >> fout, leading + ref_name
        print >> fout, (" " * (INDENT + 2)) + ref_phone
        
    print >> fout, ""
    interests = data['interests']
    for i, interest in enumerate(interests):
        lines = wrap(interest, WIDTH - INDENT - 2)
        for j, line in enumerate(lines):
            if i == 0 and j == 0:
                leading = "INTERESTS:".ljust(INDENT) + "* "
            elif j == 0:
                leading = (" " * (INDENT)) + "* "
            else:
                leading = (" " * (INDENT)) + "  "
            print >> fout, leading + line
    fout.close()

def write_html(data, outfile_name, **options):
    public_flag = options.get('public_flag', False)
    
    resume_parts = [dedent("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>Resume - ${name}</title>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" >
    <style type="text/css">
        body {
            background-color: white;
            font: 0.9em Verdana, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6, .skills{
            margin-top: 0;
            margin-bottom: 0;
            padding-top: 0;
            padding-bottom: 0;
        }
        
        h1 {
            font: 1.5em arial, sans-serif;
            text-align: center;
        }
        #id_contact_list {
            text-align: center;
            font: 0.9em Verdana, sans-serif;
        }
        h3 {
            font: 1.3em arial, sans-serif;
            font-weight: bold;
            width: 20%;
            float: left;
            clear: left;
        }

        h4 {
            font: 1.3em arial, sans-serif;
            font-weight: bold;
            width: 20%;
            float: left;
            clear: left;
        }

        h5 {
            font: 1.2em arial, sans-serif;
            font-weight: bold;
            width: 20%;
            float: left;
            clear: left;
        }

        .section {
            float: right;
            clear: right;
            width: 70%;
            margin-right: 10%;
        }

        .section-seperator {
            float: left;
            width: 100%;
            visibility: hidden;
        }

        .skills {
            list-style-type: none;
            padding-left: 0;
            margin-left: 0;
        }

        h6 {
            font: 0.7em arial, sans-serif;
            display: inline;
            font-style: italic;
        }

        h6 + div {
            display: inline;
        }

        .position-details {
            margin-left: 0;
            padding-left: 0;
            list-style-position: inside;
        }

        .reference-details, .interest-details {
            margin-top: 0;
            padding-top: 0;
            margin-bottom: 0;
            padding-bottom: 0;
            margin-left: 0;
            padding-left: 0;
        }
        
        p {
            margin-top: 0;
            margin-bottom: 1em;
            margin-left: 0;
            margin-right: 0;
        }
    </style>
</head>
<body>
    <h1>${name}</h1>
    <hr>
""")]
    if not public_flag:
        resume_parts.append(dedent("""\
    <div id="id_contact_list">
        ${address_line_1}
        <br>
        ${address_line_2}
        <br>
        ${phone}
        <br>
        ${email}
    </div>
"""))
    else:
        resume_parts.append(dedent("""\
    <div id="id_contact_list">
        ${phone}
        <br>
        ${public_email}
    </div>
"""))
    resume_parts.append(dedent("""\
    <p>
    <div>
        <h3>Objective</h3>
        <div class="section">
            ${objective}
        </div>
        <hr class="section-seperator">
    </div>
    <div>
        <h3>Education</h3>
        <div class="section">
            ${degree}, ${field}
            <br>
            ${institution}, ${institution_location}, ${graduation_year}
        </div>
        <hr class="section-seperator">
    </div>
    <div>
        <h3>Computer Skills</h3>
        <div class="section">
            <ul class="skills">
                <li>
                    <h6>Tools and Languages</h6>
                    <div>
                        ${computer_languages}
                    </div>
                </li>
                <li>
                    <h6>Platforms</h6>
                    <div>
                        ${computer_platforms}
                    </div>
                </li>
            </ul>
        </div>
        <hr class="section-seperator">
    </div>
"""))
    resume = ''.join(resume_parts)
    
    template = string.Template(resume)
    personal = data['personal']
    education = data['education']
    result = template.substitute({
                'name': personal['name'],
                'address_line_1': personal['address_line_1'],
                'address_line_2': personal['address_line_2'],
                'phone': personal['phone'],
                'email': personal['email'],
                'public_email': personal['public_email'],
                'objective': data['objective'],
                'degree': education['degree'],
                'field': education['field'],
                'institution': education['institution'],
                'institution_location': education['location'],
                'graduation_year': education['graduation_year'],
                'computer_languages': ', '.join(data['computer_skills']),
                'computer_platforms': ', '.join(data['platforms'])
                })
    fout = open(outfile_name, "w")
    fout.write(result)

    text = dedent(r"""
    <div>
        <h4>Experience</h4>
        <div class="section">
            <span>${position_name}</span>
            <span class="month-year">${month} ${year}</span>
            <br>
            ${organization}
            <br>
            ${location}
            <br>
            <ul class="position-details">
""")
    position_template = string.Template(text)
    #Previous positions held.
    experience = data['experience']
    for position in experience:
        output = position_template.substitute({
                'position_name': position.get('position', ''),
                'month': position.get('month', ''),
                'year': position['year'],
                'organization': position['organization'],
                'location': position.get('location', ''),
                })
        fout.write(output)
        details = position['details']
        for detail in details:
            fout.write("                <li>\n")
            fout.write("                    %s\n" % detail)
            fout.write("                </li>\n")
        fout.write("            </ul>\n")
        fout.write("        </div>\n")
        fout.write('        <hr class="section-seperator">\n')
        fout.write("    </div>\n")

    if not public_flag:
        references = data['references']
        fout.write("""\
        <div>
            <h5>References</h5>
            <div class="section">
                <ul class="reference-details">
    """)
        for reference in references:
            fout.write("                <li>\n")
            fout.write("                    %s<br>\n" % reference['name'])
            fout.write("                    %s\n" % reference['phone'])
            fout.write("                </li>\n")
        fout.write("            </ul>\n")
        fout.write("        </div>\n")
        fout.write('        <hr class="section-seperator">\n')
        fout.write("    </div>\n")
    else:
        fout.write("""\
            <div>
                <h5>References</h5>
                <p class="section">
                Available upon request.
                </p>
            </div>
        """)
    
    interests = data['interests']
    fout.write("""\
    <div>
        <h5>Interests</h5>
        <div class="section">
            <ul class="interest-details">
""")
    fout.write("\n")
    for interest in interests:
        fout.write("                <li>\n")
        fout.write("                    %s\n" % interest)
        fout.write("                </li>\n")
    fout.write("            </ul>\n")
    fout.write("        </div>\n")
    fout.write('        <hr class="section-seperator">\n')
    fout.write("    </div>\n")

    fout.write("</body>\n</html>\n")
    fout.close()

def escape_latex(expr):
    return unicode(expr).replace("#", "\#")

def write_latex(data, outfile_name):
    resume = dedent(r"""
% LaTeX resume using res.cls
\documentclass[margin]{res}
%\usepackage{helvetica} % uses helvetica postscript font (download helvetica.sty)
%\usepackage{newcent}   % uses new century schoolbook postscript font 
\setlength{\textwidth}{5.1in} % set width of text portion

\begin{document}

% Center the name over the entire width of resume:
 \moveleft.5\hoffset\centerline{\large\bf ${name}}
% Draw a horizontal line the whole width of resume:
 \moveleft\hoffset\vbox{\hrule width\resumewidth height 1pt}\smallskip
% address begins here
% Again, the address lines must be centered over entire width of resume:
 \moveleft.5\hoffset\centerline{${address_line_1}}
 \moveleft.5\hoffset\centerline{${address_line_2}}
 \moveleft.5\hoffset\centerline{${phone_number}}
 \moveleft.5\hoffset\centerline{${email_address}}


\begin{resume}
\hyphenation{districts}
\section{OBJECTIVE}  ${objective}
 
\section{EDUCATION} {\sl ${degree},} ${field_of_study} \\
                      % \sl will be bold italic in New Century Schoolbook (or
                  % any postscript font) and just slanted in
              % Computer Modern (default) font
                ${institution}, ${institution_location}, 
                ${graduation_year} 
 
\section{COMPUTER \\ SKILLS} 
    {\sl Tools and Languages:} 
        ${computer_languages}\\
        {\sl Platforms:} 
        ${computer_platforms}
""")
    template = string.Template(resume)
    personal = data['personal']
    education = data['education']
    result = template.substitute({
                'name': escape_latex(personal['name']),
                'address_line_1': escape_latex(personal['address_line_1']),
                'address_line_2': escape_latex(personal['address_line_2']),
                'phone_number': escape_latex(personal['phone']),
                'email_address': escape_latex(personal['email']),
                'objective': escape_latex(data['objective']),
                'degree': escape_latex(education['degree']),
                'field_of_study': escape_latex(education['field']),
                'institution': escape_latex(education['institution']),
                'institution_location': escape_latex(education['location']),
                'graduation_year': escape_latex(education['graduation_year']),
                'computer_languages': escape_latex(', '.join(data['computer_skills'])),
                'computer_platforms': escape_latex(', '.join(data['platforms']))
                })
    fout = open(outfile_name, "w")
    fout.write(result)
    
    text = dedent(r"""
\section{EXPERIENCE} {\sl ${position_name}} \hfill ${month} ${year} \\
                ${organization}, 
                ${location} \\
""")
    position_template = string.Template(text)
    #Previous positions held.
    experience = data['experience']
    for position in experience:
        output = position_template.substitute({
                'position_name': escape_latex(position.get('position', '')),
                'month': escape_latex(position.get('month', '')),
                'year': escape_latex(position['year']),
                'organization': escape_latex(position['organization']),
                'location': escape_latex(position.get('location', '')),
                })
        fout.write(output)
        details = position['details']
        fout.write(r"       \begin{itemize}  \itemsep -2pt %reduce space between items")
        fout.write("\n")
        for detail in details:
            fout.write(r"       \item %s" % escape_latex(detail))
            fout.write("\n")
        fout.write(r"                \end{itemize}")
        fout.write("\n\n")
    
    references = data['references']
    fout.write(r"\section{References}")
    fout.write("\n")
    for reference in references:
        fout.write(r"       %s\\" % escape_latex(reference['name']))
        fout.write("\n")
        fout.write(r"       %s\\" % escape_latex(reference['phone']))
        fout.write("\n")
        fout.write("\n")
    
    interests = data['interests']
    fout.write(r"\section{Interests}")
    fout.write("\n")
    for interest in interests:
        fout.write(r"           %s\\" % escape_latex(interest))
        fout.write("\n")
    
    fout.write(r"\end{resume}")
    fout.write("\n")
    fout.write(r"\end{document}")
    fout.write("\n")
    fout.close()

def usage():
    print >> sys.stderr, "Usage: %s <data.yaml> <outfile>" % sys.argv[0]
    print >> sys.stderr, dedent("""\
-- Options --
-h, --help
-V, --version
-p, --public                            ; Output is to be published on a public
                                        ; web site.  Some personal information
                                        ; will be excluded.

""".strip())

if __name__ == "__main__":
    #Defaults
    public_flag = False
    #Process command line options and arguments.
    try:
        opts, argv = getopt.gnu_getopt(sys.argv[1:],
                'hVp', [
                    'help',
                    'version',
                    'public',])
    except getopt.GetoptError, e:
        print >> sys.stderr, e.msg
        usage(sys.argv[0])
        sys.exit(STATUS_ERROR)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-V', '--version'):
            print >> sys.stderr, '1.0'
            sys.exit(0)
        elif opt in ('-p', '--public'):
            public_flag = True
        else:
            print >> sys.stderr, "Unknown option, %s." % opt
            usage()
            sys.exit(1)
            
    if len(argv) != 2:
        usage()
        sys.exit(1)
    file_name = argv[0]
    outfile_name = argv[1]
    run(file_name, outfile_name, 
        public_flag=public_flag)


