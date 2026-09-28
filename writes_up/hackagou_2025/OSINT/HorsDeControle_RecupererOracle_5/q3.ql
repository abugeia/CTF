[out:json][timeout:300][bbox:-39.0,172.5,-34.3,178.6];
(nwr["amenity"="fuel"];nwr["shop"~"convenience|general"];)->.f;
nwr["leisure"="playground"](around.f:200)->.p;
(nwr.f(around.p:200);)->.g;
way["natural"="coastline"](around.g:200)->.c;
nwr.g(around.c:200);
out center tags;
