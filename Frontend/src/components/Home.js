// // Home.js
// import React from 'react';
// import Header from './Header';
// import Footer from './Footer';
// import '../styles/home.css';
// import '../styles/header.css';


// const Home = () => {
//     return (
//         <div>
//             <main>
//             <Header />


//                 <section className="recent-posts">
//                     <div className="header">Recent Posts</div>
//                     <div className="subheader">Mindfulness, Meditation and</div>
//                     <div className="subheader-1">Everything in Between</div>
//                     <div className="content-box">
//                         <h2>Check back soon</h2>
//                     </div>
//                     <a className="more-posts" href="/more-posts">More Posts</a>
//                 </section>

                

//                 <section className="container-1">
//                     <div className="content-3">
//                         <div className="image">
//                             <img alt="Portrait of a woman" height="400" src="https://storage.googleapis.com/a1aa/image/Q18a2P39fnThWS3vLKTIRxmH7mUNWrusSJjomqh2uMvC9YfTA.jpg" width="400" />
//                         </div>
//                         <div className="text">
//                             <h1>Meet Melody Mate</h1>
//                             <p>Welcome to Melody Mate! We're your guide to discovering the perfect music for every mood. Whether you're feeling happy, relaxed, or energized, we'll help you find the perfect soundtrack to enhance your experience.</p>
//                             <a className="learn-more" href="/learn-more">Learn More</a>
//                         </div>
//                     </div>
//                 </section>
//                 <section className="hero-section">
//                     <div className="content">
//                         <h1>Express Yourself: Find the Perfect Tune for Every Feeling!</h1>
//                         <h2>Music gives a soul to the universe, wings to the mind, flight to the imagination....</h2>
//                         <h3>Capture Your Mood, Discover Your Soundtrack!</h3>
//                         <div className="button-container">
//                             <a href="/capture-mood" className="btn btn-primary">Capture Mood</a>
//                             <button type="button">Upload Photo</button>
//                         </div>
//                     </div>
//                     <div className="hero-image">
//                         <img src="/images/Cover photo.avif" width="600" alt="Cover" />
//                     </div>
//                 </section>

//                 <section className="container-2">
//                     <img alt="Abstract logo" className="logo" height="100" src="/images/flower.png" width="100" />
//                     <div className="quote">"Our life is shaped by our mind,</div>
//                     <div className="quote-1">for we become what we think."</div>
//                     <div className="author">Buddha</div>
//                 </section>
//             </main>
//             <Footer />
//         </div>
//     );
// };

// export default Home;


import React,{useRef,useState,useEffect} from 'react';
import Header from './Header';
import Footer from './Footer';
import '../styles/home.css';
import '../styles/header.css';
import '../styles/footer.css';
import { Link } from 'react-router-dom';

const HomePage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mood, setMood] = useState('');
  const [songRecommendation, setSongRecommendation] = useState(null);
  const hiddenFileInput = useRef(null);
  const [showFloatingWindow, setShowFloatingWindow] = useState(false);

  useEffect(() => {
    document.body.className = 'home-page-body'; // Add this class to the body
    return () => {
      document.body.className = ''; // Clean up the class when the component unmounts
    };
  }, []);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        setSelectedFile(file);
        uploadPhoto(file); // Automatically upload the photo when selected
    }  };

  const uploadPhoto = async (file) => {
    

      setLoading(true);
      const formData=new FormData();
      formData.append('file',file);
      try {
          const response = await fetch('http://localhost:5000/upload_photo', {
              method: 'POST',
              body: formData,
          });

          const data = await response.json();
          setMood(data.emotion); // Assuming the API returns the detected mood
          setSongRecommendation(data.song); // Assuming the API returns a song recommendation
          setShowFloatingWindow(true); // Show the floating window
      } catch (error) {
          console.error("Error uploading photo:", error);
      } finally {
          setLoading(false);
      }
  };

  const handleButtonClick = () => {
      hiddenFileInput.current.click();
  };
    return (
      <div>
        
        <Header />
  
        <main>
          <div className="hero-section">
            <div className="content">
              <h1>Express Yourself: Find the Perfect Tune for Every Feeling!</h1>
              <h2>Music gives a soul to the universe, wings to the mind, flight to the imagination....</h2>
              <h3>Capture Your Mood, Discover Your Soundtrack!</h3>
              <div className="button-container">
                <Link to="/capture-mood" className="btn">Capture Mood</Link>
                {/* <button type="button" onClick={uploadPhoto}>Upload Photo</button> */}
                <button className="btn" type="button" onClick={handleButtonClick}>
                    {loading ? "Uploading..." : "Upload Photo"}
                </button>
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    ref={hiddenFileInput}
                    style={{ display: 'none' }} // Hide the file input
                />
                          
              </div>
            </div>
            <div className="hero-image">
              <img src="/images/Cover photo.avif" width="600" alt="Cover" />
            </div>
          </div>
          {showFloatingWindow && songRecommendation && ( // Check if songRecommendation is not null
                    <div className="floating-window">
                        <button className="close-button" onClick={() => setShowFloatingWindow(false)}>X</button>

                        <h2>Detected Mood: {mood}</h2>
                        <h3>Recommended Song: {songRecommendation.song_name}</h3>
                        <img src={songRecommendation.cover_url} alt={`${songRecommendation.song_name} cover`} width="200" />
                        <p>Artist: {songRecommendation.artist_name}</p>
                        <p>Album: {songRecommendation.album_name}</p> {/* Display album name */}

                        <a href={songRecommendation.spotify_url} target="_blank" rel="noopener noreferrer">Listen on Spotify</a>
                    </div>
                )}
           
          <section className="recent-posts">
            <div className="header">Recent Posts</div>
            <div className="subheader">Mindfulness, Meditation and</div>
            <div className="subheader-1">Everything in Between</div>
            <div className="content-box">
              <h2>Check back soon</h2>
            </div>
            <a className="more-posts" href="#">More Posts</a>
          </section>
  
          <section className="container-1">
            <div className="content-3">
              <div className="image">
                <img alt="Portrait of a woman" height="400" src="https://storage.googleapis.com/a1aa/image/Q18a2P39fnThWS3vLKTIRxmH7mUNWrusSJjomqh2uMvC9YfTA.jpg" width="400" />
              </div>
              <div className="text">
                <h1>Meet Melody Mate</h1>
                <p>Welcome to Melody Mate! We're your guide to discovering the perfect music for every mood. Whether you're feeling happy, relaxed, or energized, we'll help you find the perfect soundtrack to enhance your experience.</p>
                <a className="learn-more" href="/chatbot">Learn More</a>
              </div>
            </div>
          </section>
  
          <section className="container-2">
            <img alt="Abstract logo" className="logo" height="100" src="/images/flower.png" width="100" />
            <div className="quote">"Our life is shaped by our mind,</div>
            <div className="quote-1">for we become what we think."</div>
            <div className="author">Buddha</div>
          </section>
        </main>
  
        <div className="menu-icon">
          <i className="fa-solid fa-bars"></i>
        </div>
  
        <aside className="social-links">
          <a href="#"><img src="/images/F.png" alt="Facebook" /></a>
          <a href="#"><img src="/images/T.webp" alt="Twitter" /></a>
          <a href="#"><img src="/images/Instagram.png" alt="Instagram" /></a>
        </aside>
  
       
        <Footer />
      </div>
    );
  };
  
  export default HomePage;