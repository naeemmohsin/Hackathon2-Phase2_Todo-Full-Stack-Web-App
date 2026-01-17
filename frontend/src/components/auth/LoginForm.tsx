'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Button from '../ui/Button';
import Input from '../ui/Input';
import ErrorMessage from '../ui/ErrorMessage';
import { login } from '@/lib/auth';
import { authValidation } from '@/lib/auth-client';

/**
 * LoginForm - Better Auth integrated sign-in form
 *
 * This component uses Better Auth validation patterns while
 * delegating authentication to the existing FastAPI backend.
 * JWT tokens are stored in localStorage on successful login.
 */
export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState<{
    email?: string;
    password?: string;
  }>({});
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Validate form fields using Better Auth validation rules
   */
  const validateForm = (): boolean => {
    const errors: typeof fieldErrors = {};

    // Email validation
    if (!email) {
      errors.email = authValidation.email.required;
    } else if (!authValidation.email.pattern.value.test(email)) {
      errors.email = authValidation.email.pattern.message;
    }

    // Password validation
    if (!password) {
      errors.password = authValidation.password.required;
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  /**
   * Handle form submission - login with backend and store JWT
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setFieldErrors({});

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Call backend /auth/login endpoint
      // JWT token is automatically stored in localStorage by auth.ts
      await login({ email, password });

      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (err) {
      // Handle specific error cases
      const errorMessage = err instanceof Error ? err.message : 'Login failed';

      if (errorMessage.toLowerCase().includes('invalid') ||
          errorMessage.toLowerCase().includes('incorrect') ||
          errorMessage.toLowerCase().includes('wrong')) {
        setError('Invalid email or password. Please try again.');
      } else if (errorMessage.toLowerCase().includes('not found') ||
                 errorMessage.toLowerCase().includes('no user')) {
        setError('No account found with this email. Please sign up first.');
      } else {
        setError(errorMessage || 'Login failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white shadow-lg rounded-lg px-8 py-10">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
          Sign in to your account
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <ErrorMessage message={error} />

          <Input
            label="Email address"
            type="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
            autoComplete="email"
            error={fieldErrors.email}
          />

          <Input
            label="Password"
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
            autoComplete="current-password"
            error={fieldErrors.password}
          />

          <Button
            type="submit"
            className="w-full"
            isLoading={isLoading}
          >
            Sign in
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Don&apos;t have an account?{' '}
          <Link
            href="/register"
            className="font-medium text-primary-600 hover:text-primary-500"
          >
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
