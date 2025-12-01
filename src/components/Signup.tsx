import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { UserPlus, ArrowLeft } from 'lucide-react';

interface SignupProps {
  onSignupSuccess: () => void;
  onBackToLogin: () => void;
}

export default function Signup({ onSignupSuccess, onBackToLogin }: SignupProps) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState<'Organization' | 'Civilian'>('Civilian');
  const [errors, setErrors] = useState<{ confirmPassword?: string }>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate passwords match
    if (password !== confirmPassword) {
      setErrors({ confirmPassword: 'Passwords do not match' });
      return;
    }
    
    // Backend endpoint: POST /signup
    // Payload: { name, email, password, role }
    console.log('Signup attempt:', { name, email, password, role });
    alert('Account created successfully! Please login.');
    onSignupSuccess();
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-[#004D99] to-[#003d7a]">
      <Card className="w-full max-w-md shadow-2xl border-0">
        <CardHeader className="space-y-1 pb-6">
          <Button 
            variant="ghost" 
            onClick={onBackToLogin}
            className="w-fit -ml-2 mb-2 text-[#004D99] hover:text-[#003d7a] hover:bg-blue-50"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Login
          </Button>
          <CardTitle className="text-2xl text-[#004D99]">Create Your Account</CardTitle>
          <CardDescription>Join the DPR Evaluation System</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name" className="text-slate-700">Full Name</Label>
              <Input
                id="name"
                name="name"
                type="text"
                placeholder="Enter your full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="h-11 border-slate-300 focus:border-[#004D99] focus:ring-[#004D99]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-slate-700">Email Address</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="your.email@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="h-11 border-slate-300 focus:border-[#004D99] focus:ring-[#004D99]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-slate-700">Password</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="Create a strong password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (errors.confirmPassword) setErrors({});
                }}
                required
                className="h-11 border-slate-300 focus:border-[#004D99] focus:ring-[#004D99]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="text-slate-700">Confirm Password</Label>
              <Input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                placeholder="Re-enter your password"
                value={confirmPassword}
                onChange={(e) => {
                  setConfirmPassword(e.target.value);
                  if (errors.confirmPassword) setErrors({});
                }}
                required
                className={`h-11 border-slate-300 focus:border-[#004D99] focus:ring-[#004D99] ${
                  errors.confirmPassword ? 'border-red-500' : ''
                }`}
              />
              {errors.confirmPassword && (
                <p className="text-sm text-red-500">{errors.confirmPassword}</p>
              )}
            </div>

            <div className="space-y-3 pt-2">
              <Label className="text-slate-700">Select Your Role</Label>
              <RadioGroup value={role} onValueChange={(value) => setRole(value as 'Organization' | 'Civilian')}>
                <div className="flex items-center space-x-3 p-3 rounded-lg border border-slate-300 hover:border-[#004D99] hover:bg-blue-50 transition-colors">
                  <RadioGroupItem value="Organization" id="org-signup" className="text-[#004D99]" />
                  <Label htmlFor="org-signup" className="flex-1 cursor-pointer">
                    Organization (MoDoNER)
                  </Label>
                </div>
                <div className="flex items-center space-x-3 p-3 rounded-lg border border-slate-300 hover:border-[#004D99] hover:bg-blue-50 transition-colors">
                  <RadioGroupItem value="Civilian" id="civ-signup" className="text-[#004D99]" />
                  <Label htmlFor="civ-signup" className="flex-1 cursor-pointer">
                    Civilian
                  </Label>
                </div>
              </RadioGroup>
            </div>

            <Button 
              type="submit" 
              className="w-full h-11 bg-[#004D99] hover:bg-[#003d7a] text-white shadow-md mt-6"
            >
              <UserPlus className="mr-2 h-4 w-4" />
              Create Account
            </Button>
          </form>
        </CardContent>
      </Card>
      
      <div className="mt-8 text-center">
        <p className="text-white/90 text-sm">
          Powered by AI Evaluation System
        </p>
      </div>
    </div>
  );
}