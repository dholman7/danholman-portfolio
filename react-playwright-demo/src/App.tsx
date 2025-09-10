import { useState } from 'react'
import { Mail, Lock, Eye, EyeOff, CheckCircle, AlertCircle, ArrowRight, Sparkles } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import clsx from 'clsx'

// Validation schema
const registerSchema = z.object({
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
  terms: z.boolean().refine(val => val === true, 'You must accept the terms and conditions')
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type RegisterFormData = z.infer<typeof registerSchema>

// Mock API functions
const mockRegister = async (data: RegisterFormData) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // Log the registration attempt (using the data parameter)
  console.log('Registration attempt for:', data.email)
  
  // Simulate random success/failure for demo
  if (Math.random() > 0.1) {
    return { success: true, message: 'Account created successfully!' }
  } else {
    return { success: false, message: 'Email already exists. Please try a different email.' }
  }
}

const mockLogin = async (email: string, password: string) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // Log the login attempt (using the parameters)
  console.log('Login attempt for:', email, 'with password length:', password.length)
  
  // Simulate random success/failure for demo
  if (Math.random() > 0.2) {
    return { success: true, message: 'Login successful!' }
  } else {
    return { success: false, message: 'Invalid email or password.' }
  }
}

function App() {
  const [isLogin, setIsLogin] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    // Check if user is already authenticated from session storage
    return sessionStorage.getItem('isAuthenticated') === 'true'
  })
  const [user, setUser] = useState(() => {
    // Get user data from session storage
    const userData = sessionStorage.getItem('user')
    return userData ? JSON.parse(userData) : null
  })

  const { register, handleSubmit, formState: { errors }, reset } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema)
  })

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    setMessage(null)
    
    try {
      if (isLogin) {
        const result = await mockLogin(data.email, data.password)
        setMessage({ type: result.success ? 'success' : 'error', text: result.message })
        if (result.success) {
          const userData = {
            email: data.email,
            firstName: 'User', // In a real app, this would come from the API
            loginTime: new Date().toISOString()
          }
          setUser(userData)
          setIsAuthenticated(true)
          // Store authentication state in session storage
          sessionStorage.setItem('isAuthenticated', 'true')
          sessionStorage.setItem('user', JSON.stringify(userData))
        }
      } else {
        const result = await mockRegister(data)
        setMessage({ type: result.success ? 'success' : 'error', text: result.message })
        if (result.success) {
          const userData = {
            email: data.email,
            firstName: data.firstName,
            lastName: data.lastName,
            loginTime: new Date().toISOString()
          }
          setUser(userData)
          setIsAuthenticated(true)
          // Store authentication state in session storage
          sessionStorage.setItem('isAuthenticated', 'true')
          sessionStorage.setItem('user', JSON.stringify(userData))
        }
      }
    } catch {
      setMessage({ type: 'error', text: 'An unexpected error occurred. Please try again.' })
    } finally {
      setIsLoading(false)
    }
  }

  const toggleMode = () => {
    setIsLogin(!isLogin)
    setMessage(null)
    reset()
  }

  if (isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
        {/* Header */}
        <header className="bg-white border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <span className="text-xl font-bold text-slate-900">HolmanTech</span>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-slate-600">Welcome, {user?.firstName || 'User'}!</span>
                <button
                  onClick={() => {
                    setIsAuthenticated(false)
                    setIsLogin(false)
                    setUser(null)
                    reset()
                    sessionStorage.removeItem('isAuthenticated')
                    sessionStorage.removeItem('user')
                  }}
                  className="text-slate-600 hover:text-slate-900 font-medium transition-colors"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Welcome Card */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
                <h1 className="text-3xl font-bold text-slate-900 mb-4">
                  Welcome to your HolmanTech Dashboard
                </h1>
                <p className="text-slate-600 text-lg mb-6">
                  You've successfully authenticated! This is a demo dashboard showcasing modern authentication flows.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-slate-50 rounded-xl p-4">
                    <h3 className="font-semibold text-slate-900 mb-2">Account Status</h3>
                    <p className="text-sm text-slate-600">Active and verified</p>
                  </div>
                  <div className="bg-slate-50 rounded-xl p-4">
                    <h3 className="font-semibold text-slate-900 mb-2">Last Login</h3>
                    <p className="text-sm text-slate-600">
                      {user?.loginTime ? new Date(user.loginTime).toLocaleString() : 'Just now'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button className="w-full text-left p-3 rounded-lg hover:bg-slate-50 transition-colors border border-slate-200">
                    <div className="font-medium text-slate-900">View Profile</div>
                    <div className="text-sm text-slate-600">Manage your account settings</div>
                  </button>
                  <button className="w-full text-left p-3 rounded-lg hover:bg-slate-50 transition-colors border border-slate-200">
                    <div className="font-medium text-slate-900">Security</div>
                    <div className="text-sm text-slate-600">Update password and security</div>
                  </button>
                  <button className="w-full text-left p-3 rounded-lg hover:bg-slate-50 transition-colors border border-slate-200">
                    <div className="font-medium text-slate-900">Support</div>
                    <div className="text-sm text-slate-600">Get help and contact us</div>
                  </button>
                </div>
              </div>

              {/* Demo Info */}
              <div className="bg-blue-50 rounded-2xl border border-blue-200 p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">Demo Information</h3>
                <p className="text-sm text-blue-700 mb-3">
                  This is a portfolio demonstration of modern authentication flows using React, TypeScript, and Tailwind CSS.
                </p>
                <div className="text-xs text-blue-600">
                  <p>• Session-based authentication</p>
                  <p>• Form validation with Zod</p>
                  <p>• Responsive design</p>
                  <p>• Modern UI components</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-12 items-center">
        {/* Left side - Branding and features */}
        <div className="hidden lg:block space-y-8">
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-slate-900">HolmanTech</span>
            </div>
            <h1 className="text-5xl font-bold text-slate-900 leading-tight">
              {isLogin ? 'Welcome back' : 'Get started with HolmanTech'}
            </h1>
            <p className="text-xl text-slate-600 leading-relaxed">
              {isLogin 
                ? 'Sign in to continue your journey with our platform.' 
                : 'Join thousands of users who trust HolmanTech for their business needs.'
              }
            </p>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center gap-3 text-slate-600">
              <CheckCircle className="w-5 h-5 text-emerald-500" />
              <span>Secure and reliable platform</span>
            </div>
            <div className="flex items-center gap-3 text-slate-600">
              <CheckCircle className="w-5 h-5 text-emerald-500" />
              <span>24/7 customer support</span>
            </div>
            <div className="flex items-center gap-3 text-slate-600">
              <CheckCircle className="w-5 h-5 text-emerald-500" />
              <span>Advanced analytics dashboard</span>
            </div>
          </div>
        </div>

        {/* Right side - Form */}
        <div className="bg-white rounded-3xl shadow-2xl border border-slate-200/50 p-8 lg:p-12">
          <div className="text-center mb-8">
            <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center">
              <img 
                src="/tech_logo.png" 
                alt="Tech Logo" 
                className="w-full h-full object-contain"
                data-testid="tech-logo"
              />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 mb-3">
              {isLogin ? 'Welcome back' : 'Create your account'}
            </h2>
            <p className="text-slate-600 text-lg">
              {isLogin ? 'Sign in to your account' : 'Get started with a free account'}
            </p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {!isLogin && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-3">
                    First Name
                  </label>
                  <div className="relative">
                    <input
                      {...register('firstName')}
                      type="text"
                      className={clsx(
                        'w-full px-4 py-4 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50/50',
                        errors.firstName ? 'border-red-300 bg-red-50/50' : 'border-slate-200 hover:border-slate-300'
                      )}
                      placeholder="John"
                      data-testid="first-name-input"
                    />
                  </div>
                  {errors.firstName && (
                    <p className="mt-2 text-sm text-red-600 flex items-center gap-1" data-testid="first-name-error">
                      <AlertCircle className="w-4 h-4" />
                      {errors.firstName.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-3">
                    Last Name
                  </label>
                  <div className="relative">
                    <input
                      {...register('lastName')}
                      type="text"
                      className={clsx(
                        'w-full px-4 py-4 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50/50',
                        errors.lastName ? 'border-red-300 bg-red-50/50' : 'border-slate-200 hover:border-slate-300'
                      )}
                      placeholder="Doe"
                      data-testid="last-name-input"
                    />
                  </div>
                  {errors.lastName && (
                    <p className="mt-2 text-sm text-red-600 flex items-center gap-1" data-testid="last-name-error">
                      <AlertCircle className="w-4 h-4" />
                      {errors.lastName.message}
                    </p>
                  )}
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  {...register('email')}
                  type="email"
                  className={clsx(
                    'w-full pl-12 pr-4 py-4 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50/50',
                    errors.email ? 'border-red-300 bg-red-50/50' : 'border-slate-200 hover:border-slate-300'
                  )}
                  placeholder="john@example.com"
                  data-testid="email-input"
                />
              </div>
              {errors.email && (
                <p className="mt-2 text-sm text-red-600 flex items-center gap-1" data-testid="email-error">
                  <AlertCircle className="w-4 h-4" />
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  {...register('password')}
                  type={showPassword ? 'text' : 'password'}
                  className={clsx(
                    'w-full pl-12 pr-14 py-4 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50/50',
                    errors.password ? 'border-red-300 bg-red-50/50' : 'border-slate-200 hover:border-slate-300'
                  )}
                  placeholder="Enter your password"
                  data-testid="password-input"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                  data-testid="toggle-password"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && (
                <p className="mt-2 text-sm text-red-600 flex items-center gap-1" data-testid="password-error">
                  <AlertCircle className="w-4 h-4" />
                  {errors.password.message}
                </p>
              )}
            </div>

            {!isLogin && (
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">
                  Confirm Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    {...register('confirmPassword')}
                    type={showConfirmPassword ? 'text' : 'password'}
                    className={clsx(
                      'w-full pl-12 pr-14 py-4 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50/50',
                      errors.confirmPassword ? 'border-red-300 bg-red-50/50' : 'border-slate-200 hover:border-slate-300'
                    )}
                    placeholder="Confirm your password"
                    data-testid="confirm-password-input"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                    data-testid="toggle-confirm-password"
                  >
                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-2 text-sm text-red-600 flex items-center gap-1" data-testid="confirm-password-error">
                    <AlertCircle className="w-4 h-4" />
                    {errors.confirmPassword.message}
                  </p>
                )}
              </div>
            )}

            {!isLogin && (
              <div className="flex items-start gap-3">
                <div className="flex items-center h-6">
                  <input
                    {...register('terms')}
                    type="checkbox"
                    className="w-5 h-5 text-blue-600 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:ring-2"
                    data-testid="terms-checkbox"
                  />
                </div>
                <div className="text-sm">
                  <label className="text-slate-700 leading-relaxed">
                    I agree to the{' '}
                    <a href="#" className="text-blue-600 hover:text-blue-700 font-semibold underline underline-offset-2">
                      Terms and Conditions
                    </a>{' '}
                    and{' '}
                    <a href="#" className="text-blue-600 hover:text-blue-700 font-semibold underline underline-offset-2">
                      Privacy Policy
                    </a>
                  </label>
                  {errors.terms && (
                    <p className="mt-2 text-sm text-red-600 flex items-center gap-1" data-testid="terms-error">
                      <AlertCircle className="w-4 h-4" />
                      {errors.terms.message}
                    </p>
                  )}
                </div>
              </div>
            )}

            {message && (
              <div className={clsx(
                'p-4 rounded-xl flex items-center gap-3 border',
                message.type === 'success' 
                  ? 'bg-emerald-50 text-emerald-800 border-emerald-200' 
                  : 'bg-red-50 text-red-800 border-red-200'
              )} data-testid="message">
                {message.type === 'success' ? (
                  <CheckCircle className="w-5 h-5 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                )}
                <span className="font-medium">{message.text}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className={clsx(
                'w-full py-4 px-6 rounded-xl font-semibold transition-all duration-200 flex items-center justify-center gap-2 group',
                isLoading
                  ? 'bg-slate-300 cursor-not-allowed text-slate-500'
                  : 'bg-slate-900 hover:bg-slate-800 text-white hover:shadow-lg hover:shadow-slate-900/25'
              )}
              data-testid="submit-button"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-slate-500 border-t-transparent rounded-full animate-spin"></div>
                  Please wait...
                </>
              ) : (
                <>
                  {isLogin ? 'Sign in' : 'Create account'}
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-slate-600">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                onClick={toggleMode}
                className="text-slate-900 hover:text-slate-700 font-semibold underline underline-offset-2 transition-colors"
                data-testid="toggle-mode"
              >
                {isLogin ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App