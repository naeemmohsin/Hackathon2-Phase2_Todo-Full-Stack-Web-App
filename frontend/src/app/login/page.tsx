import LoginForm from '@/components/auth/LoginForm';

export const metadata = {
  title: 'Sign In - Todo App',
  description: 'Sign in to your Todo account',
};

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <LoginForm />
    </div>
  );
}
