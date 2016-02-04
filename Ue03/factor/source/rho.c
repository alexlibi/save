// Pollard-Rho-Verfahren mit n Iterationen ohne Speicherung der Iterierten (zufaelliger Startwert).
void rho(mpz_t number, mpz_t factor, int n)
{
	mpz_t a, x, y, z, diff, rnd;
	mpz_init_set_ui(a, 1);
	mpz_init_set_ui(x, 1);
	mpz_init_set_ui(y, 1);
	mpz_init_set_ui(z, 1);
	mpz_init_set_ui(diff, 0);
	mpz_init_set_ui(rnd, rand());
	mpz_add(x, x, rnd);
	mpz_add(y, y, rnd);
	int i, iter = 0;
	
	while (iter < n)
	{
		iter += 50;
		mpz_set_ui(z, 1);
		for (i = 1; i <= 50; i++)
		{
			mpz_mul(x, x, x);
			mpz_add(x, x, a);
			mpz_mod(x, x, number);
			mpz_mul(y, y, y);
			mpz_add(y, y, a);
			mpz_mod(y, y, number);
			mpz_mul(y, y, y);
			mpz_add(y, y, a);
			mpz_mod(y, y, number);
			mpz_sub(diff, y, x);
			mpz_mul(z, z, diff);
			mpz_mod(z, z, number);
		}
		mpz_gcd(factor, z, number);
		if (mpz_cmp_si(factor, 1) != 0) break;
	}
	
	mpz_clear(a);
	mpz_clear(x);
	mpz_clear(y);
	mpz_clear(z);
	mpz_clear(diff);
	mpz_clear(rnd);
}
