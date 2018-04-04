
/* Ver actividad criminal en un periodo de tiempo */
select * from incidents.overall 
 where time >= '2017-01-01 00:00:00' and time <= dateof(now()) 
 allow filtering;

/* Buscar incidencia */
select * from incidents.overall 
where year in (2017,2016,2015) incidentId = 150098975;

/* Actividad criminal por zonas (año 2017) */
select district, year, incidentid, category, time, location 
 from incidents.bydistrict 
 where year = 2017;

/* Actividad criminal por zonas desde la mitad del año hasta la actualidad */
select district, year, incidentid, category, time, location 
 from incidents.bydistrict 
 where year = 2018 and time >= '2018-06-01 00:00:00' and time <= dateof(now())
 allow filtering;

/* Actividad criminal para categoria (año 2017). */
select category, year, incidentid, category, time, location 
 from incidents.bycategory 
 where year = 2017;

/* Actividad criminal para zonas en el mes de Enero (año 2017)*/
select year, district, count(*) 
 from incidents.bydistrict
 where year = 2017 and month = 1 
 group by district 
 allow filtering;

/* Agregados de incidencias en zonas / por año */
select year, district, count(*) 
 from incidents.bydistrict
 where year = 2017 and month = 1 
 group by district 
 allow filtering;

/* Agregados de incidencias de categorias / por año */
select category, year, count(*) 
 from incidents.bycategory 
 where year = 2017
 group by category;


