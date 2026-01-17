'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Button from '../ui/Button';
import Input from '../ui/Input';
import ErrorMessage from '../ui/ErrorMessage';
import { register } from '@/lib/auth';
import { authValidation } from '@/lib/auth-client';

/**
 * RegisterForm - Better Auth integrated sign-up form
 *
 * This component uses Better Auth validation patterns while
 * delegating authentication to the existing FastAPI backend.
 * JWT tokens are stored in localStorage on successful registration.
 */
export default function RegisterForm() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState<{
    email?: string;
    password?: string;
    confirmPassword?: string;
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
    } else if (password.length < authValidation.password.minLength.value) {
      errors.password = authValidation.password.minLength.message;
    }

    // Confirm password validation
    if (password !== confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  /**
   * Handle form submission - register with backend and store JWT
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
      // Call backend /auth/register endpoint
      // JWT token is automatically stored in localStorage by auth.ts
      await register({ email, password });

      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (err) {
      // Handle specific error cases
      const errorMessage = err instanceof Error ? err.message : 'Registration failed';

      if (errorMessage.toLowerCase().includes('already registered') ||
          errorMessage.toLowerCase().includes('already exists')) {
        setError('An account with this email already exists. Please sign in instead.');
      } else if (errorMessage.toLowerCase().includes('password')) {
        setFieldErrors({ password: errorMessage });
      } else if (errorMessage.toLowerCase().includes('email')) {
        setFieldErrors({ email: errorMessage });
      } else {
        setError(errorMessage || 'Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white shadow-lg rounded-lg px-8 py-10">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
          Create your account
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
            placeholder="At least 8 characters"
            required
            autoComplete="new-password"
            error={fieldErrors.password}
          />

          <Input
            label="Confirm password"
            type="password"
            name="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
            autoComplete="new-password"
            error={fieldErrors.confirmPassword}
          />

          <Button
            type="submit"
            className="w-full"
            isLoading={isLoading}
          >
            Create account
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link
            href="/login"
            className="font-medium text-primary-600 hover:text-primary-500"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
