# json payload values
values can be null (None), or each or all items in corresponding list

- **age_certifications**: null or country specific list
- **content_types**: null or [movie, show]
- **presentation_types**: null or [hd, sd]
- **providers**: null or [mbi, qfs, tpl, msf, pls, ply, itu, ddi, crk, qfx, prs, stn, nfx]
- **genres**: null or [act, ani, cmy, crm, drm, msc, hrr, hst, fnt, trl, war, wsn, rma, scf,doc, fml, spt]
- **languages**: null
- **release_year_from**: null or year > 1900
- **release_year_until**: null or year < current year
- **monetization_types**: null or [flatrate, ads, rent, buy, free, cinema]
- **min_price**: null or integer value
- **max_price**: null or integer value,
- **nationwide_cinema_releases_only**: null or True or False
- **scoring_filter_types**: null or
  - **imdb:score**
    - **min_scoring_value**: 0.0
    - **max_scoring_value**: 10.0
  - **tomato:meter**
    - **min_scoring_value**: 0
    - **max_scoring_value**: 100
- **cinema_release**: null
- **query**: null or title as string
- **page**: null or integer value
- **page_size**: null or integer value
- **timeline_type**: TBC

# shortened values
## providers
- **mbi**: mubi
- **qfs**: quickflix store
- **tpl**: tenplay
- **msf**: micrsoft
- **pls**: playstation
- **ply**: google play store
- **itu**: itunes
- **ddi**: dendy direct
- **crk**: crackle
- **qfx**: quickflix
- **prs**: presto
- **stn**: stan
- **nfx**: netflix

## genres
- **act**: action
- **ani**: animation
- **cmy**: comedy
- **crm**: crime
- **drm**: drama
- **msc**: music and musical
- **hrr**: horror
- **hst**: history
- **fnt**: fantasy
- **trl**: mystery and thriller 
- **war**: war
- **wsn**: western
- **rma**: romance
- **scf**: scifi
- **doc**: documentary
- **fml**: kids and family
- **spt**: sport