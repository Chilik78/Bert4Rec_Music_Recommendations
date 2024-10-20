import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Registration, Entry, MainWindow } from './components/components';
import './styles/App.css'

function App() {
  return (
    <Router>
      <div className="App">
              <Routes>
                <Route exact path='/' element={<Entry/>} />
                <Route path='/reg' element={<Registration/>} />
                <Route path='/main' element={<MainWindow/>} />
                <Route path="*" element={<Navigate to="/" />}/>
              </Routes>  
      </div>
    </Router>
  );
}

export default App;