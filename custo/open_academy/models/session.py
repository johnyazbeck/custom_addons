from odoo import api, fields, models

class OpenAcademySession(models.Model):
    _name = "open.academy.session"
    _description = "Session"
    _rec_name = "display_name_calc"  # <- on affiche ce champ partout

    course_id = fields.Many2one("open.academy.course", string="Cours", required=True)
    date_start = fields.Date(string="Date")
    attendee_ids = fields.Many2many("res.partner", string="Participants")

    # Un seul champ calculé pour l'affichage
    display_name_calc = fields.Char(
        string="Nom à afficher",
        compute="_compute_display_name_calc",
        store=True,            # stocké
        compute_sudo=True,     # et on fixe le même compute_sudo partout
        index=True,
    )

    @api.depends("course_id.name", "date_start")
    def _compute_display_name_calc(self):
        for rec in self:
            course = rec.course_id.name or "Sans cours"
            date = rec.date_start.strftime("%d/%m/%Y") if rec.date_start else "Sans date"
            rec.display_name_calc = f"Session {course} – {date}"
