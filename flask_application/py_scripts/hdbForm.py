from wtforms import *

class HDB(Form):
    block = StringField('Block', validators=[validators.DataRequired(), validators.Length(min=1, max=5)], render_kw={"placeholder": "123A"})
    street_name = StringField('Street Name', validators=[validators.DataRequired()], render_kw={"placeholder": "Sengakang East Way"})
    town = SelectField('Town', validators=[validators.DataRequired()], choices=[])
    postal_code = StringField('Postal Code', validators=[validators.DataRequired()], render_kw={"placeholder": "123456"})
    month = DateField('Estimated Month of Purchase', validators=[validators.DataRequired()])
    storey_range = SelectField('Resale Flat Storey Range', validators=[validators.DataRequired()], choices=[])
    floor_area_sqm = DecimalField('Resale Flat Floor Area Sqm', validators=[validators.DataRequired(), validators.NumberRange(min=30, max=300)])
    flat_model = SelectField('Resale Flat Model', validators=[validators.DataRequired()], choices=[])
    lease_commence_date = StringField('Lease Commence Date', validators=[validators.DataRequired(), validators.Length(min=4, max=4)])
    cbd_dist = DecimalField('Central Business District (CBD) Distance from HDB in meters', validators=[validators.DataRequired()], 
                            render_kw={"placeholder": "500"})
    min_dist_mrt = DecimalField('MRT Distance from HDB in meters', validators=[validators.DataRequired()], render_kw={"placeholder": "5"})