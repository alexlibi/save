// Berechnet curves elliptische Kurven mit den Parametern B1 und B2.
void ecm(mpz_t number, mpz_t factor, int B1, int B2, int curves)
{
	// Datenfeld fuer einen Kurvenpunkt.
	struct CPoint
	{
		mpz_t x;
		mpz_t y;
	};

	// Aus Performancegruenden (Vermeidung von mpz_init() bzw. mpz_clear()) werden alle lokalen Variablen hier deklariert.
	mpz_t a, ac, xdiff, sigma, su, su2, inv3, inv4, aold, xold, t, temp;
	mpz_init(a);
	mpz_init(ac);
	mpz_init(xdiff);
	mpz_init(sigma);
	mpz_init(su);
	mpz_init(su2);
	mpz_init_set_si(inv3, 3);
	mpz_init_set_si(inv4, 4);
	mpz_init(aold);
	mpz_init(xold);
	mpz_init(t);
	mpz_init(temp);
	mpz_invert(inv3, inv3, number);
	mpz_invert(inv4, inv4, number);
	struct CPoint p, prod, wp, kwp, kp;
	mpz_init(p.x);
	mpz_init(p.y);
	mpz_init(prod.x);
	mpz_init(prod.y);
	mpz_init(wp.x);
	mpz_init(wp.y);
	mpz_init(kwp.x);
	mpz_init(kwp.y);
	mpz_init(kp.x);
	mpz_init(kp.y);

	mpz_t alpha, xx, yy, xpy2, xmy2, xy4, t1, t2, t1pt2, t1mt2, qxy;
	mpz_init(alpha);
	mpz_init(xx);
	mpz_init(yy);
	mpz_init(xpy2);
	mpz_init(xmy2);
	mpz_init(xy4);
	mpz_init(t1);
	mpz_init(t2);
	mpz_init(t1pt2);
	mpz_init(t1mt2);
	mpz_init(qxy);
	struct CPoint q, sum, dbl, p0, p2, q0;
	mpz_init(q.x);
	mpz_init(q.y);
	mpz_init(sum.x);
	mpz_init(sum.y);
	mpz_init(dbl.x);
	mpz_init(dbl.y);
	mpz_init(p0.x);
	mpz_init(p0.y);
	mpz_init(p2.x);
	mpz_init(p2.y);
	mpz_init(q0.x);
	mpz_init(q0.y);

	// Punktaddition in Weierstrassform.
	void wAdd(struct CPoint *p, struct CPoint *q, struct CPoint *sum, mpz_t number, mpz_t factor, mpz_t a)
	{
		if ((mpz_cmp((*p).x, (*q).x) == 0) && (mpz_cmp((*p).y, (*q).y) == 0))
		{
			mpz_mul_2exp(yy, (*p).y, 1);
			// Addition unmoeglich: Faktor gefunden!
			if (mpz_invert(yy, yy, number) == 0)
			{
				mpz_gcd(factor, yy, number);
				return;
			}
			mpz_mul(alpha, (*p).x, (*p).x);
			mpz_mul_si(alpha, alpha, 3);
			mpz_add(alpha, alpha, a);
			mpz_mul(alpha, alpha, yy);
			mpz_mod(alpha, alpha, number);
		}
		else
		{
			mpz_sub(xx, (*q).x, (*p).x);
			// Addition unmoeglich: Faktor gefunden!
			if (mpz_invert(xx, xx, number) == 0)
			{
				mpz_gcd(factor, xx, number);
				return;
			}
			mpz_sub(alpha, (*q).y, (*p).y);
			mpz_mul(alpha, alpha, xx);
			mpz_mod(alpha, alpha, number);
		}

		mpz_mul((*sum).x, alpha, alpha);
		mpz_sub((*sum).x, (*sum).x, (*p).x);
		mpz_sub((*sum).x, (*sum).x, (*q).x);
		mpz_mod((*sum).x, (*sum).x, number);
		mpz_sub((*sum).y, (*p).x, (*sum).x);
		mpz_mul((*sum).y, (*sum).y, alpha);
		mpz_sub((*sum).y, (*sum).y, (*p).y);
		mpz_mod((*sum).y, (*sum).y, number);
	}

	// Berechnet das k-fache eines Punktes in Weierstrassform.
	void wMult(int k, struct CPoint *p, struct CPoint *prod, mpz_t number, mpz_t factor, mpz_t a)
	{
		mpz_set(q.x, (*p).x);
		mpz_set(q.y, (*p).y);

		char setprod = 1;

		// Schrittweise Addition durch das "Binary Ladder"-Verfahren.
		while (k != 0)
		{
			if ((k % 2) == 1)
				if (setprod == 1)
				{
					mpz_set((*prod).x, q.x);
					mpz_set((*prod).y, q.y);
					setprod = 0;
				}
				else
				{
					wAdd(prod, &q, &sum, number, factor, a);
					mpz_set((*prod).x, sum.x);
					mpz_set((*prod).y, sum.y);
				}
			k = (k >> 1);
			wAdd(&q, &q, &sum, number, factor, a);
			mpz_set(q.x, sum.x);
			mpz_set(q.y, sum.y);
		}
	}

	// Punktverdopplung in Montgomeryform.
	void mDouble(struct CPoint *p, struct CPoint *dbl, mpz_t number, mpz_t ac)
	{
		mpz_add(xpy2, (*p).x, (*p).y);
		mpz_mul(xpy2, xpy2, xpy2);
		mpz_sub(xmy2, (*p).x, (*p).y);
		mpz_mul(xmy2, xmy2, xmy2);
		mpz_sub(xy4, xpy2, xmy2);
		mpz_mul((*dbl).x, xpy2, xmy2);
		mpz_mod((*dbl).x, (*dbl).x, number);
		mpz_mul((*dbl).y, ac, xy4);
		mpz_add((*dbl).y, (*dbl).y, xmy2);
		mpz_mul((*dbl).y, (*dbl).y, xy4);
		mpz_mod((*dbl).y, (*dbl).y, number);
	}

	// Punktaddition in Montgomeryform.
	void mAdd(struct CPoint *p, struct CPoint *q, struct CPoint *d, struct CPoint *sum, mpz_t number)
	{
		mpz_sub(t1, (*p).x, (*p).y);
		mpz_add(qxy, (*q).x, (*q).y);
		mpz_mul(t1, t1, qxy);
		mpz_add(t2, (*p).x, (*p).y);
		mpz_sub(qxy, (*q).x, (*q).y);
		mpz_mul(t2, t2, qxy);
		mpz_add(t1pt2, t1, t2);
		mpz_sub(t1mt2, t1, t2);
		mpz_mul((*sum).x, t1pt2, t1pt2);
		mpz_mul((*sum).x, (*sum).x, (*d).y);
		mpz_mod((*sum).x, (*sum).x, number);
		mpz_mul((*sum).y, t1mt2, t1mt2);
		mpz_mul((*sum).y, (*sum).y, (*d).x);
		mpz_mod((*sum).y, (*sum).y, number);
	}

	// Berechnet das m-fache eines Punktes in Montgomeryform.
	void mMult(int m, struct CPoint *p, struct CPoint *p1, mpz_t number, mpz_t ac)
	{
		mpz_set((*p1).x, (*p).x);
		mpz_set((*p1).y, (*p).y);
		while ((m % 2) == 0)
		{
			mDouble(p1, &dbl, number, ac);
			mpz_set((*p1).x, dbl.x);
			mpz_set((*p1).y, dbl.y);
			m = (m >> 1);
		}
		if (m == 1) return;

		mpz_set(p0.x, (*p1).x);
		mpz_set(p0.y, (*p1).y);

		mDouble(p1, &p2, number, ac);
		int biti = 1;
		while (biti <= m)
			biti = (biti << 1);
		biti = (biti >> 2);
		// Schrittweise Addition durch das "Binary Ladder"-Verfahren.
		while (biti > 1)
		{
			mAdd(&p2, p1, &p0, &q0, number);
			if ((m & biti) > 0)
			{
				mpz_set((*p1).x, q0.x);
				mpz_set((*p1).y, q0.y);
				mDouble(&p2, &dbl, number, ac);
				mpz_set(p2.x, dbl.x);
				mpz_set(p2.y, dbl.y);
			}
			else
			{
				mDouble(p1, &dbl, number, ac);
				mpz_set((*p1).x, dbl.x);
				mpz_set((*p1).y, dbl.y);
				mpz_set(p2.x, q0.x);
				mpz_set(p2.y, q0.y);
			}
			biti = (biti >> 1);
		}

		mAdd(&p2, p1, &p0, &dbl, number);
		mpz_set((*p1).x, dbl.x);
		mpz_set((*p1).y, dbl.y);
	}

	// Berechnet die (abgerundete) Quadratwurzel einer ganzen Zahl.
	int root(int n)
	{
		int r = n, s = 1;
		int i;
		do
		{
			r = (r + s + 1)/2;
			s = n/r;
		}
		while (r - s > 1);
		return s;
	}

	int s, u, v, w = root(B2);
	int x1len = B2/w + 2, x2len = w + 1;
	int i, j;
	char *primes = (char*) malloc(B2 + 1);
	mpz_t x1arr[x1len], x2arr[x2len];

	// Initialisierungen + Erstellung der Primzahltabelle.
	for (i = 2; i <= B2; i++)
		primes[i] = 1;
	for (i = 2; i <= w; i++)
		if (primes[i] == 1)
		{
			j = i + i;
			while (j <= B2)
			{
				primes[j] = 0;
				j += i;
			}
		}
	for (i = 1; i < x1len; i++)
		mpz_init(x1arr[i]);
	for (i = 1; i < x2len; i++)
		mpz_init(x2arr[i]);

	mpz_set_si(factor, 1);

	// Berechnung einer weiteren Kurve.
	while ((curves > 0) && (mpz_cmp_si(factor, 1) == 0))
	{
		curves--;

		// Kurve generieren + Startpunkt berechnen.
		mpz_set_si(sigma, rand());
		mpz_mul(su, sigma, sigma);
		mpz_add_ui(su, su, 6);
		mpz_invert(su, su, number);
		mpz_mul(su, su, sigma);
		mpz_mul_si(su, su, 6);
		mpz_mod(su, su, number);
		mpz_mul(su2, su, su);
		mpz_mod(su2, su2, number);

		mpz_mul_si(factor, su2, 9);
		mpz_sub_ui(factor, factor, 10);
		mpz_mul(factor, factor, su2);
		mpz_add_ui(factor, factor, 1);
		mpz_mul(factor, factor, su);
		mpz_gcd(factor, factor, number);
		if (mpz_cmp_si(factor, 1) != 0) goto final;

		mpz_mul_si(a, su2, 3);
		mpz_add_ui(a, a, 6);
		mpz_mul(a, a, su2);
		mpz_set_si(temp, 1);
		mpz_sub(a, temp, a);
		mpz_mul(a, a, inv4);
		mpz_mul(temp, su2, su);
		mpz_invert(temp, temp, number);
		mpz_mul(a, a, temp);
		mpz_mod(a, a, number);
		mpz_add_ui(ac, a, 2);
		mpz_mul(ac, ac, inv4);
		mpz_mod(ac, ac, number);
		mpz_mul_si(p.x, su, 3);
		mpz_mul(p.x, p.x, inv4);
		mpz_mod(p.x, p.x, number);
		mpz_set_si(p.y, 1);

		// Phase 0: Multiplikation mit Vielfachen kleinerer Primzahlen fuer hinreichende Glattheit.
		for (i = 11; i <= 39; i++)
		{
			mMult(i, &p, &prod, number, ac);
			mpz_set(p.x, prod.x);
			mpz_set(p.y, prod.y);
		}
		mpz_gcd(factor, p.y, number);
		if (mpz_cmp_si(factor, 1) != 0) goto final;

		// Phase 1: Multiplikation mit allen Primzahlen <= B1.
		for (i = 17; i <= B1; i++)
			if (primes[i] == 1)
			{
				mMult(i, &p, &prod, number, ac);
				mpz_set(p.x, prod.x);
				mpz_set(p.y, prod.y);
			}
		mpz_gcd(factor, p.y, number);
		if (mpz_cmp_si(factor, 1) != 0) goto final;

		// Umrechnung in die Weierstrassform.
		mpz_set(aold, a);
		mpz_invert(xold, p.y, number);
		mpz_mul(xold, xold, p.x);
		mpz_mod(xold, xold, number);
		mpz_add(t, xold, aold);
		mpz_mul(t, t, xold);
		mpz_add_ui(t, t, 1);
		mpz_mul(t, t, xold);
		mpz_mod(t, t, number);
		mpz_invert(p.y, t, number);
		mpz_set_si(temp, 1);
		mpz_mul(a, aold, aold);
		mpz_mul(a, a, inv3);
		mpz_sub(a, temp, a);
		mpz_mul(a, a, p.y);
		mpz_mul(a, a, p.y);
		mpz_mod(a, a, number);
		mpz_mul(p.x, aold, inv3);
		mpz_add(p.x, p.x, xold);
		mpz_mul(p.x, p.x, p.y);
		mpz_mod(p.x, p.x, number);

		// Tabellen mit den Primzahldifferenzen erzeugen.
		wMult(w, &p, &wp, number, factor, a);
		mpz_set(kwp.x, wp.x);
		mpz_set(kwp.y, wp.y);
		for (i = 1; i < x1len; i++)
		{
			mpz_set(x1arr[i], kwp.x);
			wAdd(&kwp, &wp, &prod, number, factor, a);
			mpz_set(kwp.x, prod.x);
			mpz_set(kwp.y, prod.y);
		}
		mpz_set(kp.x, p.x);
		mpz_set(kp.y, p.y);
		for (i = 1; i < x2len; i++)
		{
			mpz_set(x2arr[i], kp.x);
			wAdd(&kp, &p, &prod, number, factor, a);
			mpz_set(kp.x, prod.x);
			mpz_set(kp.y, prod.y);
		}
		int index = B1;
		while (primes[index] == 0)
			index--;
		v = (index / w) + 1;
		u = w - (index % w);
		mpz_set_si(xdiff, 1);
		s = 0;

		// Phase 2: Nach der BigPrime suchen.
		for (i = index + 1; i <= B2; i++)
		{
			if (primes[i] == 0) continue;
			s++;
			u -= (i - index);
			if (u <= 0)
			{
				u += w;
				v++;
			}
			mpz_sub(temp, x1arr[v], x2arr[u]);
			mpz_mul(xdiff, xdiff, temp);
			mpz_mod(xdiff, xdiff, number);
			if (s == 240)
			{
				mpz_gcd(factor, xdiff, number);
				if (mpz_cmp_si(factor, 1) != 0) goto final;
				mpz_set_si(xdiff, 1);
				s = 0;
			}
			index = i;
		}
		mpz_gcd(factor, xdiff, number);
	}

	// Speicherfreigabe.
	final:
	free(primes);
	mpz_clear(a);
	mpz_clear(ac);
	mpz_clear(xdiff);
	mpz_clear(sigma);
	mpz_clear(su);
	mpz_clear(su2);
	mpz_clear(inv3);
	mpz_clear(inv4);
	mpz_clear(aold);
	mpz_clear(xold);
	mpz_clear(t);
	mpz_clear(temp);
	mpz_clear(p.x);
	mpz_clear(p.y);
	mpz_clear(prod.x);
	mpz_clear(prod.y);
	mpz_clear(wp.x);
	mpz_clear(wp.y);
	mpz_clear(kwp.x);
	mpz_clear(kwp.y);
	mpz_clear(kp.x);
	mpz_clear(kp.y);
	for (i = 1; i < x1len; i++)
		mpz_clear(x1arr[i]);
	for (i = 1; i < x2len; i++)
		mpz_clear(x2arr[i]);

	mpz_clear(alpha);
	mpz_clear(xx);
	mpz_clear(yy);
	mpz_clear(xpy2);
	mpz_clear(xmy2);
	mpz_clear(xy4);
	mpz_clear(t1);
	mpz_clear(t2);
	mpz_clear(t1pt2);
	mpz_clear(t1mt2);
	mpz_clear(qxy);
	mpz_clear(q.x);
	mpz_clear(q.y);
	mpz_clear(sum.x);
	mpz_clear(sum.y);
	mpz_clear(dbl.x);
	mpz_clear(dbl.y);
	mpz_clear(p0.x);
	mpz_clear(p0.y);
	mpz_clear(p2.x);
	mpz_clear(p2.y);
	mpz_clear(q0.x);
	mpz_clear(q0.y);
}
