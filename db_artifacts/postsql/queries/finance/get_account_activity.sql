select
	aa.id,
	aa.product_id,
	aa.customer_id,
	aa.account_id,
	aa.amt_usd,
	aa.post_date,
	dc.channel_desc,
	dp.partner_desc,
	geo.location_name,
	gl.account_name,
	gl.account_type
from fin_account_activity aa

join fin_distro_channel dc
	on 
	aa.fin_distro_channel_id = dc.id
join fin_distro_partner dp
	on 
	aa.fin_distro_partner_id = dp.id
join geo_geography geo
	on
	geo.id = aa.geo_geography_id
join fin_gl_accounts gl
  on gl.id = aa.account_id
