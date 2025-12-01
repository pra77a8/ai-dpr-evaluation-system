import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Sheet, SheetContent } from './ui/sheet';
import { 
  LogOut, 
  MessageSquare, 
  CheckCircle, 
  MapPin,
  Star,
  Send,
  User,
  Building2,
  Clock,
  TrendingUp,
  Menu,
  ThumbsUp,
  ThumbsDown,
  Heart
} from 'lucide-react';

interface CivilianDashboardProps {
  onLogout: () => void;
}

type TabType = 'projects' | 'feedback' | 'progress' | 'all-feedback';

// Mock data
const approvedProjects = [
  {
    id: 1,
    title: 'Rural Road Development',
    summary: 'Construction of 5km rural road connecting village to main highway with proper drainage system.',
    status: 'In Progress',
    location: 'Village Rampur, District East',
    budget: '₹25 Lakhs',
    completion: 65,
    startDate: '2025-01-15',
    endDate: '2025-12-30',
  },
  {
    id: 2,
    title: 'Primary School Building',
    summary: 'New 3-story building with 12 classrooms, library, and computer lab for government primary school.',
    status: 'In Progress',
    location: 'Sector 15, District North',
    budget: '₹45 Lakhs',
    completion: 40,
    startDate: '2025-02-01',
    endDate: '2026-01-31',
  },
  {
    id: 3,
    title: 'Water Supply System',
    summary: 'Installation of overhead water tank and pipeline network covering 500 households.',
    status: 'Completed',
    location: 'Ward 7, Municipal Area',
    budget: '₹18 Lakhs',
    completion: 100,
    startDate: '2024-08-01',
    endDate: '2025-03-31',
  },
  {
    id: 4,
    title: 'Community Health Center',
    summary: 'Renovation and expansion of existing health center with new equipment and ambulance facility.',
    status: 'In Progress',
    location: 'Block Hospital Road',
    budget: '₹32 Lakhs',
    completion: 75,
    startDate: '2024-11-01',
    endDate: '2025-06-30',
  },
];

const myFeedback = [
  {
    id: 1,
    project: 'Water Supply System',
    rating: 5,
    comment: 'Excellent work! Water quality has improved significantly.',
    date: '2025-04-15',
  },
  {
    id: 2,
    project: 'Rural Road Development',
    rating: 4,
    comment: 'Good progress, but some minor delays in construction.',
    date: '2025-05-20',
  },
];

// Feedback interface
interface Feedback {
  id: string;
  dpr_id: string;
  project_title: string;
  civilian_id: string;
  civilian_name: string;
  content: string;
  submitted_at: string;
  likes_count: number;
  dislikes_count: number;
  likes: string[]; // User IDs who liked
  dislikes: string[]; // User IDs who disliked
}

const progressTimeline = [
  { phase: 'Planning & Approval', status: 'completed', date: '2025-01-15' },
  { phase: 'Site Preparation', status: 'completed', date: '2025-02-01' },
  { phase: 'Foundation Work', status: 'completed', date: '2025-03-15' },
  { phase: 'Main Construction', status: 'in-progress', date: '2025-05-01' },
  { phase: 'Finishing Work', status: 'pending', date: '2025-08-15' },
  { phase: 'Final Inspection', status: 'pending', date: '2025-10-01' },
];

export default function CivilianDashboard({ onLogout }: CivilianDashboardProps) {
  const [activeTab, setActiveTab] = useState<TabType>('projects');
  const [selectedProject, setSelectedProject] = useState(approvedProjects[0]);
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [comments, setComments] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [allFeedbacks, setAllFeedbacks] = useState<Feedback[]>([]); // New state for all feedbacks
  const [currentUser, setCurrentUser] = useState({ id: 'civilian_user_id', name: 'Current User' }); // Mock current user

  // Fetch all feedbacks when all-feedback tab is active
  useEffect(() => {
    if (activeTab === 'all-feedback') {
      fetchAllFeedbacks();
    }
  }, [activeTab]);

  const fetchAllFeedbacks = async () => {
    try {
      const response = await fetch('/api/feedback/organization/dashboard', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const feedbackData: Feedback[] = await response.json();
        setAllFeedbacks(feedbackData);
      }
    } catch (error) {
      console.error('Error fetching feedbacks:', error);
      // Fallback to sample data if fetch fails
      setAllFeedbacks([
        {
          id: '1',
          dpr_id: 'dpr1',
          project_title: 'Rural Road Development Project',
          civilian_id: 'user1',
          civilian_name: 'John Citizen',
          content: 'This project will greatly benefit our community. I hope it gets approved soon!',
          submitted_at: '2025-10-01T10:30:00Z',
          likes_count: 5,
          dislikes_count: 1,
          likes: ['user2', 'user3', 'user4', 'user5', 'user6'],
          dislikes: ['user7']
        },
        {
          id: '2',
          dpr_id: 'dpr2',
          project_title: 'School Building Project',
          civilian_id: 'user2',
          civilian_name: 'Jane Resident',
          content: 'I have concerns about the environmental impact of this project. Please consider a more eco-friendly approach.',
          submitted_at: '2025-09-28T14:15:00Z',
          likes_count: 8,
          dislikes_count: 2,
          likes: ['user1', 'user3', 'user4', 'user5', 'user6', 'user8', 'user9', 'user10'],
          dislikes: ['user11', 'user12']
        }
      ]);
    }
  };

  const handleLikeFeedback = async (feedbackId: string) => {
    try {
      const response = await fetch(`/api/feedback/${feedbackId}/like`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: currentUser.id }),
        credentials: 'include'
      });
      
      if (response.ok) {
        const updatedFeedback: Feedback = await response.json();
        // Update the feedback in the state
        setAllFeedbacks(prev => prev.map(fb => fb.id === feedbackId ? updatedFeedback : fb));
      }
    } catch (error) {
      console.error('Error liking feedback:', error);
    }
  };

  const handleDislikeFeedback = async (feedbackId: string) => {
    try {
      const response = await fetch(`/api/feedback/${feedbackId}/dislike`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: currentUser.id }),
        credentials: 'include'
      });
      
      if (response.ok) {
        const updatedFeedback: Feedback = await response.json();
        // Update the feedback in the state
        setAllFeedbacks(prev => prev.map(fb => fb.id === feedbackId ? updatedFeedback : fb));
      }
    } catch (error) {
      console.error('Error disliking feedback:', error);
    }
  };

  const handleSubmitFeedback = (e: React.FormEvent) => {
    e.preventDefault();
    // Backend endpoint: POST /feedback
    // Payload: { project: selectedProject.title, rating, comments }
    console.log('Feedback submission:', { 
      project: selectedProject.title, 
      rating, 
      comments 
    });
    alert('Feedback submitted successfully! Thank you for your input.');
    setFeedbackDialogOpen(false);
    setRating(0);
    setComments('');
  };

  const menuItems = [
    { id: 'projects' as TabType, icon: Building2, label: 'Approved Projects' },
    { id: 'feedback' as TabType, icon: MessageSquare, label: 'My Feedback' },
    { id: 'all-feedback' as TabType, icon: MessageSquare, label: 'All Feedback' },
    { id: 'progress' as TabType, icon: TrendingUp, label: 'Track Progress' },
  ];

  const SidebarContent = () => (
    <>
      <div className="p-6 border-b border-[#003d7a]">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-[#E3B23C] rounded-lg">
            <MessageSquare className="h-6 w-6 text-[#004D99]" />
          </div>
          <div>
            <h2 className="font-semibold">DPR System</h2>
            <p className="text-xs text-blue-200">Civilian Portal</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <div className="space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                setActiveTab(item.id);
                setMobileMenuOpen(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                activeTab === item.id
                  ? 'bg-[#E3B23C] text-[#004D99] shadow-lg'
                  : 'text-white hover:bg-[#003d7a]'
              }`}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </nav>

      <div className="p-4 border-t border-[#003d7a]">
        <p className="text-xs text-blue-200 mb-2">Citizen Participation</p>
      </div>
    </>
  );

  return (
    <div className="flex h-screen bg-[#F2F4F7]">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex w-64 bg-[#004D99] text-white flex-col shadow-xl">
        <SidebarContent />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
        <SheetContent side="left" className="w-64 bg-[#004D99] text-white p-0 border-0">
          <div className="flex flex-col h-full">
            <SidebarContent />
          </div>
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navigation */}
        <header className="bg-white border-b border-slate-200 shadow-sm">
          <div className="px-4 sm:px-6 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setMobileMenuOpen(true)}
                className="lg:hidden text-[#004D99]"
              >
                <Menu className="h-6 w-6" />
              </Button>
              <div>
                <h1 className="text-lg sm:text-2xl text-[#004D99]">
                  {menuItems.find(item => item.id === activeTab)?.label}
                </h1>
                <p className="text-xs sm:text-sm text-slate-500 hidden sm:block">Civilian Dashboard</p>
              </div>
            </div>
            <div className="flex items-center gap-2 sm:gap-4">
              <Avatar className="h-8 w-8 sm:h-10 sm:w-10 bg-[#004D99] cursor-pointer">
                <AvatarFallback className="bg-[#004D99] text-white">
                  <User className="h-4 w-4 sm:h-5 sm:w-5" />
                </AvatarFallback>
              </Avatar>
              <Button 
                variant="outline" 
                onClick={onLogout}
                className="border-[#004D99] text-[#004D99] hover:bg-blue-50"
                size="sm"
              >
                <LogOut className="mr-0 sm:mr-2 h-4 w-4" />
                <span className="hidden sm:inline">Logout</span>
              </Button>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-auto p-4 sm:p-6">
          {/* Approved Projects Tab */}
          {activeTab === 'projects' && (
            <div className="space-y-4 sm:space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                {approvedProjects.map((project) => (
                  <Card key={project.id} className="shadow-lg border-0 hover:shadow-xl transition-shadow">
                    <CardHeader className="pb-4">
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-2">
                        <CardTitle className="text-base sm:text-lg text-[#004D99]">{project.title}</CardTitle>
                        <Badge 
                          className={`${
                            project.status === 'Completed'
                              ? 'bg-green-100 text-green-700 hover:bg-green-100'
                              : 'bg-blue-100 text-blue-700 hover:bg-blue-100'
                          }`}
                        >
                          <CheckCircle className="h-3 w-3 mr-1" />
                          {project.status}
                        </Badge>
                      </div>
                      <CardDescription className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {project.location}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-slate-600 text-sm mb-4">{project.summary}</p>
                      
                      <div className="space-y-3">
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-slate-500">Budget:</span>
                          <span className="text-[#004D99]">{project.budget}</span>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-500">Completion</span>
                            <span className="text-[#004D99]">{project.completion}%</span>
                          </div>
                          <div className="w-full bg-slate-200 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-[#004D99] to-[#E3B23C] h-2 rounded-full transition-all"
                              style={{ width: `${project.completion}%` }}
                            />
                          </div>
                        </div>

                        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 pt-3 border-t border-slate-200">
                          <div className="text-xs text-slate-500">
                            <Clock className="h-3 w-3 inline mr-1" />
                            <span className="hidden sm:inline">{project.startDate} to {project.endDate}</span>
                            <span className="sm:hidden">Timeline: {project.startDate}</span>
                          </div>
                          <Dialog open={feedbackDialogOpen && selectedProject.id === project.id} onOpenChange={setFeedbackDialogOpen}>
                            <DialogTrigger asChild>
                              <Button
                                size="sm"
                                onClick={() => setSelectedProject(project)}
                                className="bg-[#E3B23C] hover:bg-[#d4a235] text-[#004D99] w-full sm:w-auto"
                              >
                                <MessageSquare className="h-4 w-4 mr-1" />
                                Give Feedback
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-md">
                              <DialogHeader>
                                <DialogTitle className="text-[#004D99]">Submit Feedback</DialogTitle>
                                <DialogDescription>
                                  Share your experience about {selectedProject.title}
                                </DialogDescription>
                              </DialogHeader>
                              <form onSubmit={handleSubmitFeedback} className="space-y-4 mt-4">
                                <div className="space-y-2">
                                  <Label>Rating (1-5)</Label>
                                  <div className="flex items-center gap-2">
                                    {[1, 2, 3, 4, 5].map((star) => (
                                      <button
                                        key={star}
                                        type="button"
                                        onClick={() => setRating(star)}
                                        onMouseEnter={() => setHoveredRating(star)}
                                        onMouseLeave={() => setHoveredRating(0)}
                                        className="transition-transform hover:scale-110"
                                      >
                                        <Star
                                          className={`h-7 w-7 ${
                                            star <= (hoveredRating || rating)
                                              ? 'fill-[#E3B23C] text-[#E3B23C]'
                                              : 'text-slate-300'
                                          }`}
                                        />
                                      </button>
                                    ))}
                                    {rating > 0 && (
                                      <span className="ml-2 text-slate-600">{rating}/5</span>
                                    )}
                                  </div>
                                </div>

                                <div className="space-y-2">
                                  <Label htmlFor="feedback-comments">Your Comments</Label>
                                  <Textarea
                                    id="feedback-comments"
                                    name="comments"
                                    placeholder="Share your detailed feedback..."
                                    value={comments}
                                    onChange={(e) => setComments(e.target.value)}
                                    required
                                    rows={4}
                                    className="resize-none border-slate-300 focus:border-[#004D99]"
                                  />
                                </div>

                                <Button 
                                  type="submit" 
                                  className="w-full bg-[#004D99] hover:bg-[#003d7a] text-white"
                                  disabled={rating === 0}
                                >
                                  <Send className="mr-2 h-4 w-4" />
                                  Submit Feedback
                                </Button>
                              </form>
                            </DialogContent>
                          </Dialog>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* My Feedback Tab */}
          {activeTab === 'feedback' && (
            <div className="max-w-4xl mx-auto space-y-3 sm:space-y-4">
              {myFeedback.length > 0 ? (
                myFeedback.map((feedback) => (
                  <Card key={feedback.id} className="shadow-lg border-0">
                    <CardHeader>
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2">
                        <div>
                          <CardTitle className="text-base sm:text-lg text-[#004D99]">{feedback.project}</CardTitle>
                          <CardDescription className="mt-1">
                            Submitted on {feedback.date}
                          </CardDescription>
                        </div>
                        <div className="flex items-center gap-1">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`h-4 w-4 ${
                                i < feedback.rating
                                  ? 'fill-[#E3B23C] text-[#E3B23C]'
                                  : 'text-slate-300'
                              }`}
                            />
                          ))}
                          <span className="ml-2 text-sm text-slate-600">{feedback.rating}/5</span>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-slate-700">{feedback.comment}</p>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <Card className="shadow-lg border-0">
                  <CardContent className="p-12 text-center">
                    <MessageSquare className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                    <p className="text-slate-500">You haven't submitted any feedback yet.</p>
                    <Button
                      onClick={() => setActiveTab('projects')}
                      className="mt-4 bg-[#004D99] hover:bg-[#003d7a]"
                    >
                      View Projects
                    </Button>
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {/* Track Progress Tab */}
          {activeTab === 'progress' && (
            <div className="max-w-4xl mx-auto space-y-4 sm:space-y-6">
              <Card className="shadow-lg border-0">
                <CardHeader className="bg-gradient-to-r from-[#004D99] to-[#003d7a] text-white rounded-t-lg">
                  <CardTitle>Rural Road Development - Progress Timeline</CardTitle>
                  <CardDescription className="text-blue-100">
                    Track the implementation phases of the project
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="space-y-6">
                    {progressTimeline.map((phase, index) => (
                      <div key={index} className="flex gap-4">
                        <div className="flex flex-col items-center">
                          <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center ${
                              phase.status === 'completed'
                                ? 'bg-green-500 text-white'
                                : phase.status === 'in-progress'
                                ? 'bg-[#E3B23C] text-white'
                                : 'bg-slate-200 text-slate-400'
                            }`}
                          >
                            {phase.status === 'completed' ? (
                              <CheckCircle className="h-5 w-5" />
                            ) : phase.status === 'in-progress' ? (
                              <Clock className="h-5 w-5" />
                            ) : (
                              <span className="text-sm">{index + 1}</span>
                            )}
                          </div>
                          {index < progressTimeline.length - 1 && (
                            <div
                              className={`w-0.5 h-16 ${
                                phase.status === 'completed'
                                  ? 'bg-green-500'
                                  : 'bg-slate-200'
                              }`}
                            />
                          )}
                        </div>
                        <div className="flex-1 pb-6 sm:pb-8">
                          <h3 className="text-base sm:text-lg text-[#004D99] mb-1">{phase.phase}</h3>
                          <p className="text-xs sm:text-sm text-slate-500">
                            {phase.status === 'completed'
                              ? `Completed on ${phase.date}`
                              : phase.status === 'in-progress'
                              ? `In progress since ${phase.date}`
                              : `Scheduled for ${phase.date}`}
                          </p>
                          {phase.status === 'in-progress' && (
                            <div className="mt-2">
                              <Badge className="bg-[#E3B23C] text-[#004D99] hover:bg-[#E3B23C]">
                                Currently Active
                              </Badge>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="shadow-lg border-0 bg-gradient-to-br from-blue-50 to-white">
                <CardContent className="p-6">
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-[#004D99] rounded-lg">
                      <TrendingUp className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-lg mb-2 text-[#004D99]">Stay Informed</h3>
                      <p className="text-sm text-slate-600">
                        Track the progress of government projects in your area. Get real-time updates on project milestones, 
                        completion status, and upcoming phases. Your active participation helps ensure accountability and 
                        transparency in public works.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* All Feedback Tab */}
          {activeTab === 'all-feedback' && (
            <div className="max-w-4xl mx-auto space-y-3 sm:space-y-4">
              {allFeedbacks.length > 0 ? (
                allFeedbacks.map((feedback) => (
                  <Card key={feedback.id} className="shadow-lg border-0">
                    <CardHeader>
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2">
                        <div>
                          <CardTitle className="text-base sm:text-lg text-[#004D99]">{feedback.project_title}</CardTitle>
                          <CardDescription className="mt-1">
                            Submitted by {feedback.civilian_name} on {new Date(feedback.submitted_at).toLocaleDateString()}
                          </CardDescription>
                        </div>
                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => handleLikeFeedback(feedback.id)}
                            className={`flex items-center gap-1 ${
                              feedback.likes.includes(currentUser.id) ? 'text-[#E3B23C]' : 'text-slate-300'
                            }`}
                          >
                            <ThumbsUp className="h-4 w-4" />
                            <span>{feedback.likes_count}</span>
                          </button>
                          <button
                            onClick={() => handleDislikeFeedback(feedback.id)}
                            className={`flex items-center gap-1 ${
                              feedback.dislikes.includes(currentUser.id) ? 'text-[#E3B23C]' : 'text-slate-300'
                            }`}
                          >
                            <ThumbsDown className="h-4 w-4" />
                            <span>{feedback.dislikes_count}</span>
                          </button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-slate-700">{feedback.content}</p>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <Card className="shadow-lg border-0">
                  <CardContent className="p-12 text-center">
                    <MessageSquare className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                    <p className="text-slate-500">No feedbacks available yet.</p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}