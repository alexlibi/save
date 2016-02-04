// Realisiert die Probedivision bis n.
void trial(mpz_t number, mpz_t factor, int n)
{
	mpz_set_ui(factor, 1);
	int primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29};
	int i, fac;
	
	for (i = 0; i < 10; i++)
	{
		if (mpz_divisible_ui_p(number, primes[i]) != 0)
		{
			mpz_set_ui(factor, primes[i]);
			return;
		}
	}
	
	fac = 31;
	// Probedivision durch alle zu 30 teilerfremden Zahlen.
	while (fac <= n)
	{
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 6;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 4;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 2;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 4;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 2;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 4;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 6;
		if (mpz_divisible_ui_p(number, fac) != 0) { mpz_set_ui(factor, fac); return; }
		fac += 2;
	}
}
