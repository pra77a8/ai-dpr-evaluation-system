import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Shield } from 'lucide-react';

interface LoginProps {
  onLogin: (role: 'Organization' | 'Civilian') => void;
  onGoToSignup: () => void;
}

export default function Login({ onLogin, onGoToSignup }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'Organization' | 'Civilian'>('Organization');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Backend endpoint: POST /login
    // Payload: { email, password, role }
    console.log('Login attempt:', { email, password, role });
    onLogin(role);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-[#004D99] to-[#003d7a]">
      <Card className="w-full max-w-md shadow-2xl border-0">
        <CardHeader className="space-y-3 text-center pb-6">
          <div className="flex justify-center">
            <div className="p-4 bg-gradient-to-br from-[#004D99] to-[#003d7a] rounded-2xl shadow-lg">
              <Shield className="h-10 w-10 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl text-[#004D99]">Pragati(NE)</CardTitle>
          <CardDescription className="text-base">
            Secure login to access the platform
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Demo Credentials Section */}
          <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="font-medium text-[#004D99] mb-2">Demo Credentials</h3>
            <p className="text-sm text-slate-600 mb-2">
              For judges to easily access the system:
            </p>
            <div className="text-sm space-y-1">
              <p><span className="font-medium">Username:</span> organization@gmail.com</p>
              <p><span className="font-medium">Password:</span> 7782</p>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              You can copy these credentials to login as an organization user.
            </p>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-5">
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
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="h-11 border-slate-300 focus:border-[#004D99] focus:ring-[#004D99]"
              />
            </div>

            <div className="space-y-3 pt-2">
              <Label className="text-slate-700">Select Your Role</Label>
              <RadioGroup value={role} onValueChange={(value) => setRole(value as 'Organization' | 'Civilian')}>
                <div className="flex items-center space-x-3 p-3 rounded-lg border border-slate-300 hover:border-[#004D99] hover:bg-blue-50 transition-colors">
                  <RadioGroupItem value="Organization" id="org" className="text-[#004D99]" />
                  <Label htmlFor="org" className="flex-1 cursor-pointer">
                    Organization (MoDoNER)
                  </Label>
                </div>
                <div className="flex items-center space-x-3 p-3 rounded-lg border border-slate-300 hover:border-[#004D99] hover:bg-blue-50 transition-colors">
                  <RadioGroupItem value="Civilian" id="civ" className="text-[#004D99]" />
                  <Label htmlFor="civ" className="flex-1 cursor-pointer">
                    Civilian
                  </Label>
                </div>
              </RadioGroup>
            </div>

            <div className="flex flex-col gap-3 pt-4">
              <Button 
                type="submit" 
                className="w-full h-11 bg-[#004D99] hover:bg-[#003d7a] text-white shadow-md"
              >
                Login
              </Button>
              <Button 
                type="button" 
                variant="outline" 
                onClick={onGoToSignup}
                className="w-full h-11 border-[#004D99] text-[#004D99] hover:bg-blue-50"
              >
                Sign Up
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
      
      <div className="mt-8 text-center">
        <p className="text-white/90 text-sm">
          Powered by Pragati(NE) System
        </p>
      </div>
    </div>
  );
}