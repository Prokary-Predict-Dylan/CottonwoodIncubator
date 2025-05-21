import { useState, useEffect } from 'react'
import { Button } from "/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "/components/ui/card"
import { Switch } from "/components/ui/switch"
import { Moon, Sun } from "lucide-react"
import { LineChart, XAxis, YAxis, Line, CartesianGrid, Tooltip, Legend } from "recharts"

// --- Simulated Java Classes ---
class IphoneFactory {
  constructor() {
    this.iphoneCount = 0;
    this.coins = 0;
    this.productionSpeed = 1;
    this.upgradeCost = 10;
  }

  produce() {
    this.iphoneCount += this.productionSpeed;
    this.coins += this.productionSpeed;
  }

  sell() {
    if (this.iphoneCount > 0) {
      this.iphoneCount -= 1;
      this.coins += 10;
      return "Sold 1 iPhone for 10 coins!";
    } else {
      return "No iPhones to sell!";
    }
  }

  upgrade() {
    if (this.coins >= this.upgradeCost) {
      this.coins -= this.upgradeCost;
      this.productionSpeed += 1;
      this.upgradeCost *= 2;
      return "Production speed upgraded!";
    } else {
      return "Not enough coins!";
    }
  }
}

class StockMarket {
  constructor() {
    this.stockPrice = 100;
    this.cash = 1000;
    this.stocksOwned = 0;
    this.margin = 0;
  }

  updatePrice() {
    const change = (Math.random() - 0.5) * 10;
    this.stockPrice += change;
    return this.stockPrice;
  }

  buy() {
    if (this.cash >= this.stockPrice) {
      this.cash -= this.stockPrice;
      this.stocksOwned += 1;
      return "Stock purchased!";
    } else {
      return "Not enough cash!";
    }
  }

  sell() {
    if (this.stocksOwned > 0) {
      this.cash += this.stockPrice;
      this.stocksOwned -= 1;
      return "Stock sold!";
    } else {
      return "No stocks to sell!";
    }
  }

  marginBuy() {
    if (this.cash >= this.stockPrice) {
      this.cash -= this.stockPrice;
      this.stocksOwned += 1;
      this.margin += this.stockPrice;
      return "Bought on margin!";
    } else {
      return "Not enough cash!";
    }
  }
}

// --- Main App ---
export default function App() {
  const [mode, setMode] = useState('iphone')
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light'
    setTheme(savedTheme)
    document.documentElement.classList.toggle('dark', savedTheme === 'dark')
  }, [])

  useEffect(() => {
    localStorage.setItem('theme', theme)
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  return (
      <div className="min-h-screen bg-white dark:bg-gray-900 text-black dark:text-white flex flex-col items-center justify-center p-4">
        <header className="flex items-center justify-between w-full max-w-4xl mb-8">
          <div className="flex items-center space-x-4">
            <Button variant="outline" onClick={() => setMode('iphone')}>
              iPhone Production Game
            </Button>
            <Button variant="outline" onClick={() => setMode('stock')}>
              Stock Market Simulator
            </Button>
            <Button variant="outline" onClick={() => setMode('ai-mentor')}>
              AI Mentor
            </Button>
          </div>
          <div className="flex items-center space-x-2">
            <Sun className="h-4 w-4" />
            <Switch
                checked={theme === 'dark'}
                onCheckedChange={(checked) => setTheme(checked ? 'dark' : 'light')}
            />
            <Moon className="h-4 w-4" />
          </div>
        </header>
        <main className="w-full max-w-4xl">
          {mode === 'iphone' ? <IphoneProductionGame /> : mode === 'stock' ? <StockMarketSimulator /> : <AIMentor />}
        </main>
        <footer className="mt-8">
          <EducationalSection />
        </footer>
      </div>
  )
}

function IphoneProductionGame() {
  const factory = useState(() => new IphoneFactory())[0]
  const [tick, setTick] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      factory.produce()
      setTick((prev) => prev + 1) // Force re-render
    }, 1000)
    return () => clearInterval(interval)
  }, [factory])

  return (
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>iPhone Production Game</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-lg">iPhone Count: {factory.iphoneCount}</p>
            <p className="text-lg">Coins: {factory.coins}</p>
          </div>
          <Button onClick={() => { alert(factory.sell()); setTick(tick + 1) }}>Sell iPhone</Button>
          <Button onClick={() => { alert(factory.upgrade()); setTick(tick + 1) }}>
            Upgrade Production (Cost: {factory.upgradeCost} coins)
          </Button>
        </CardContent>
      </Card>
  )
}

function StockMarketSimulator() {
  const market = useState(() => new StockMarket())[0]
  const [chartData, setChartData] = useState([])
  const [timeLeft, setTimeLeft] = useState(300)
  const [tick, setTick] = useState(0)

  useEffect(() => {
    const priceInterval = setInterval(() => {
      const newPrice = market.updatePrice()
      setChartData((prev) => [...prev, { time: new Date().toLocaleTimeString(), price: newPrice }])
      setTick((prev) => prev + 1)
    }, 1000)

    const timerInterval = setInterval(() => {
      setTimeLeft((prev) => prev - 1)
    }, 1000)

    return () => {
      clearInterval(priceInterval)
      clearInterval(timerInterval)
    }
  }, [market])

  useEffect(() => {
    if (timeLeft <= 0) {
      alert('Time is up!')
    }
  }, [timeLeft])

  return (
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Stock Market Simulator</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-lg">Stock Price: ${market.stockPrice.toFixed(2)}</p>
            <p className="text-lg">Cash: ${market.cash.toFixed(2)}</p>
          </div>
          <div className="flex items-center justify-between">
            <p className="text-lg">Stocks Owned: {market.stocksOwned}</p>
            <p className="text-lg">Margin: ${market.margin.toFixed(2)}</p>
          </div>
          <div className="flex items-center justify-between">
            <p className="text-lg">Time Left: {Math.floor(timeLeft / 60)}:{timeLeft % 60 < 10 ? '0' : ''}{timeLeft % 60}</p>
          </div>
          <div className="flex space-x-2">
            <Button onClick={() => { alert(market.buy()); setTick(tick + 1) }}>Buy Stock</Button>
            <Button onClick={() => { alert(market.sell()); setTick(tick + 1) }}>Sell Stock</Button>
            <Button onClick={() => { alert(market.marginBuy()); setTick(tick + 1) }}>Use Margin</Button>
          </div>
          <LineChart
              width={500}
              height={300}
              data={chartData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </CardContent>
      </Card>
  )
}

function EducationalSection() {
  const [sections, setSections] = useState([])

  useEffect(() => {
    const savedSections = localStorage.getItem('sections')
    if (savedSections) {
      setSections(JSON.parse(savedSections))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('sections', JSON.stringify(sections))
  }, [sections])

  const addSection = () => {
    setSections((prev) => [...prev, `Section ${sections.length + 1}`])
  }

  const removeSection = (index) => {
    setSections((prev) => prev.filter((_, i) => i !== index))
  }

  return (
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Educational Section</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button onClick={addSection}>Add Section</Button>
          {sections.map((section, index) => (
              <div key={index} className="flex items-center justify-between">
                <p className="text-lg">{section}</p>
                <Button variant="destructive" onClick={() => removeSection(index)}>
                  Remove
                </Button>
              </div>
          ))}
        </CardContent>
      </Card>
  )
}

function AIMentor() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState('')

  const askMentor = async () => {
    setResponse("Thinking...")
    const api_key = process.env.API_KEY
    try {
      const res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${api_key}`
        },
        body: JSON.stringify({
          model: "gpt-4o-mini",
          messages: [{ role: "user", content: question }],
          max_tokens: 100
        })
      });
      const data = await res.json();
      setResponse(data.choices[0].message.content);
    } catch (error) {
      setResponse("Oops! Something went wrong.");
      console.error("Error:", error);
    }
  }

  return (
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>AI Stock Mentor</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <input
                type="text"
                id="mentor-input"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Type your question here..."
                className="w-full p-2 border rounded"
            />
            <Button onClick={askMentor}>Ask</Button>
          </div>
          <div className="mt-4">
            <p className="text-lg">{response}</p>
          </div>
        </CardContent>
      </Card>
  )
}
// Dark Mode Toggle Function
const toggleSwitch = document.querySelector('.switch input[type="checkbox"]');
const body = document.body;

toggleSwitch.addEventListener('change', () => {
  if (toggleSwitch.checked) {
    body.classList.add('dark-mode');
  } else {
    body.classList.remove('dark-mode');
  }
});

// Button Click Handling - For example, to show an alert on button click
const buttons = document.querySelectorAll('button');

buttons.forEach(button => {
  button.addEventListener('click', (event) => {
    const buttonText = event.target.textContent;
    alert(`You clicked the ${buttonText} button!`);
  });
});

// Smooth Scroll for Navigation (Example: If you had anchor links)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
import { useState, useEffect } from 'react';
import { Button } from "/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "/components/ui/card";
import { Sun, Moon, ChevronRight, Play, BookOpen, BarChart2, Users, Shield } from "lucide-react";
import { Switch } from "/components/ui/switch";
import { Label } from "/components/ui/label";
import Chart from 'chart.js/auto';

export default function StockMarketApp() {
  const [darkMode, setDarkMode] = useState(false);
  const [currentSection, setCurrentSection] = useState('home');
  const [storyStep, setStoryStep] = useState(1);
  const [iphoneCount, setIphoneCount] = useState(0);
  const [coins, setCoins] = useState(0);
  const [stockPrice, setStockPrice] = useState(100);
  const [cash, setCash] = useState(1000);
  const [stocksOwned, setStocksOwned] = useState(0);
  const [popupOpen, setPopupOpen] = useState(false);
  const [popupContent, setPopupContent] = useState({ title: '', description: '' });
  const [mentorQuestion, setMentorQuestion] = useState('');
  const [mentorResponse, setMentorResponse] = useState('');

  // Toggle dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Story mode navigation
  const nextStoryStep = (step: number) => {
    setStoryStep(step);
  };

  // Show popup for ethical issues
  const showPopup = (title: string, description: string) => {
    setPopupContent({ title, description });
    setPopupOpen(true);
  };

  // iPhone production game functions
  const produceIPhone = () => {
    setIphoneCount(prev => prev + 1);
    setCoins(prev => prev + 5);
  };

  const sellIPhones = () => {
    if (iphoneCount > 0) {
      setCoins(prev => prev + iphoneCount * 10);
      setIphoneCount(0);
    }
  };

  // Stock market simulator functions
  const buyStock = () => {
    if (cash >= stockPrice) {
      setCash(prev => prev - stockPrice);
      setStocksOwned(prev => prev + 1);
    }
  };

  const sellStock = () => {
    if (stocksOwned > 0) {
      setCash(prev => prev + stockPrice);
      setStocksOwned(prev => prev - 1);
    }
  };

  // AI Mentor function
  const askMentor = () => {
    // In a real app, you would call an API here
    setMentorResponse(`Answer to "${mentorQuestion}" would appear here from an AI service`);
  };

  return (
      <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-white'}`}>
        {/* Header with theme toggle */}
        <header className="p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Stock Market Learning App</h1>
          <div className="flex items-center space-x-2">
            <Sun className="h-5 w-5" />
            <Switch
                id="dark-mode"
                checked={darkMode}
                onCheckedChange={setDarkMode}
            />
            <Moon className="h-5 w-5" />
            <Label htmlFor="dark-mode">Switch Theme</Label>
          </div>
        </header>

        {/* Main content */}
        <main className="container mx-auto px-4 py-8">
          {/* Home Screen */}
          {currentSection === 'home' && (
              <Card>
                <CardHeader>
                  <CardTitle>Welcome to the Stock Market Learning App</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <Button onClick={() => setCurrentSection('ethical-issues')}>Ethical Issues</Button>
                  <Button onClick={() => setCurrentSection('employment-impact')}>Employment Impact</Button>
                  <Button onClick={() => setCurrentSection('key-takeaways')}>Key Takeaways</Button>
                  <Button onClick={() => setCurrentSection('story-mode')}>Story Mode</Button>
                  <Button onClick={() => setCurrentSection('game-mode')}>Game Mode</Button>
                  <Button onClick={() => setCurrentSection('test-your-knowledge')}>Test Your Knowledge</Button>
                  <Button onClick={() => setCurrentSection('summary')}>Summary</Button>
                  <Button onClick={() => setCurrentSection('ai-mentor')}>AI Mentor</Button>
                  <Button onClick={() => setCurrentSection('market-crashes')}>Market Crashes</Button>
                  <Button onClick={() => setCurrentSection('stock-myths')}>Stock Market Myths</Button>
                  <Button onClick={() => setCurrentSection('etfs-vs-mutuals')}>ETFs vs. Mutual Funds</Button>
                </CardContent>
              </Card>
          )}

          {/* Story Mode */}
          {currentSection === 'story-mode' && (
              <Card>
                <CardHeader>
                  <CardTitle>Story Mode</CardTitle>
                  <CardDescription>Embark on an interactive journey to build your stock market skills!</CardDescription>
                </CardHeader>
                <CardContent>
                  {storyStep === 1 && (
                      <div className="space-y-4">
                        <h3 className="text-lg font-medium">Step 1: Starting Out</h3>
                        <p>You have $10,000 to invest. Choose wisely!</p>
                        <div className="flex gap-4">
                          <Button onClick={() => nextStoryStep(2)}>Invest in a Tech Company</Button>
                          <Button onClick={() => nextStoryStep(3)}>Invest in Renewable Energy</Button>
                        </div>
                      </div>
                  )}
                  {/* Add other story steps similarly */}
                  <Button onClick={() => setCurrentSection('home')} className="mt-4">Back to Home</Button>
                </CardContent>
              </Card>
          )}

          {/* Game Mode */}
          {currentSection === 'game-mode' && (
              <Card>
                <CardHeader>
                  <CardTitle>Game Mode</CardTitle>
                </CardHeader>
                <CardContent className="space-y-8">
                  <div>
                    <h3 className="text-lg font-medium mb-4">iPhone Production Game</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p>iPhones Produced: {iphoneCount}</p>
                        <p>Coins: {coins}</p>
                      </div>
                      <div className="space-y-2">
                        <Button onClick={produceIPhone}>Produce an iPhone</Button>
                        <Button onClick={sellIPhones}>Sell iPhones</Button>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-medium mb-4">Stock Market Simulator</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p>Stock Price: ${stockPrice.toFixed(2)}</p>
                        <p>Cash: ${cash.toFixed(2)}</p>
                        <p>Stocks Owned: {stocksOwned}</p>
                      </div>
                      <div className="space-y-2">
                        <Button onClick={buyStock}>Buy Stock</Button>
                        <Button onClick={sellStock}>Sell Stock</Button>
                      </div>
                    </div>
                  </div>
                  <Button onClick={() => setCurrentSection('home')}>Back to Home</Button>
                </CardContent>
              </Card>
          )}

          {/* Market Crashes Section */}
          {currentSection === 'market-crashes' && (
              <Card>
                <CardHeader>
                  <CardTitle>Historical Market Crashes</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-4">
                    <li>
                      <strong>1929 - The Great Depression:</strong> Caused by rampant speculation and buying stocks on borrowed money.
                      <p className="text-sm italic">What to do: Don't over-leverage your investments.</p>
                    </li>
                    {/* Add other crashes similarly */}
                  </ul>
                  <Button onClick={() => setCurrentSection('home')} className="mt-4">Back to Home</Button>
                </CardContent>
              </Card>
          )}

          {/* AI Mentor Section */}
          {currentSection === 'ai-mentor' && (
              <Card>
                <CardHeader>
                  <CardTitle>AI Stock Mentor</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <input
                        type="text"
                        value={mentorQuestion}
                        onChange={(e) => setMentorQuestion(e.target.value)}
                        placeholder="Ask your question..."
                        className="flex-1 border rounded px-3 py-2"
                    />
                    <Button onClick={askMentor}>Ask</Button>
                  </div>
                  {mentorResponse && (
                      <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded">
                        <p>{mentorResponse}</p>
                      </div>
                  )}
                  <Button onClick={() => setCurrentSection('home')}>Back to Home</Button>
                </CardContent>
              </Card>
          )}

          {/* Add other sections similarly */}
        </main>

        {/* Popup for ethical issues */}
        {popupOpen && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
              <Card className="w-full max-w-md">
                <CardHeader className="flex flex-row justify-between items-center">
                  <CardTitle>{popupContent.title}</CardTitle>
                  <button onClick={() => setPopupOpen(false)} className="text-gray-500 hover:text-gray-700">
                    &times;
                  </button>
                </CardHeader>
                <CardContent>
                  <p>{popupContent.description}</p>
                </CardContent>
              </Card>
            </div>
        )}
      </div>
  );
}

