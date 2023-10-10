	select SUM(amt_usd) as product_total,
	product_id
	from public.fin_account_activity
	group by product_id
	order by sum desc;
