// src/components/Footer.js
import React from 'react';
import '../styles/footer.css'; // Import your footer styles

// const Footer = () => {
//     return (
//         <footer className="footer">
//             <div>
//                 <div className="footer-logo-icon">🎵</div>
//                 <div className="footer-logo-text">
//                     <span className="footer-logo-emotion">Emo</span>
//                     <span className="footer-logo-song">Song</span>
//                 </div>
//                 <p>My mindfulness blog</p>
//             </div>
//             <div>
//                 <form>
//                     <p>Get my daily tips on mindful living</p>
//                     <label htmlFor="email">Email *</label>
//                     <input id="email" name="email" required type="email" />
//                     <label>
//                         <input name="subscribe" type="checkbox" />
//                         Yes, subscribe me to your newsletter.
//                     </label>
//                     <button type="submit">Subscribe</button>
//                 </form>
//             </div>
//             <div>
//                 <p>Breathe by Tammy Gallaway</p>
//                 <p>Mail: info@mysite.com</p>
//                 <p>Phone number: 123-456-7890</p>
//             </div>
//             <div className="footer-bottom">
//                 <p>
//                     © 2035 by Tammy Gallaway. Powered and secured by
//                     <a href="https://www.wix.com" style={{ color: '#FFFFFF' }}>
//                         EmoSong
//  </a>
//                 </p>
//             </div>
//         </footer>
//     );
// };

const Footer = () => {
    return (
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-logo-icon">🎵</div>
          <div className="footer-logo-text">
            <span className="footer-logo-emotion">Emo</span>
            <span className="footer-logo-song">Song</span>
          </div>
          <p>My mindfulness blog</p>
        </div>
        <div className="footer-subscription">
          <form>
            <p>Get my daily tips on mindful living</p>
            <label htmlFor="email">Email *</label>
            <input id="email" name="email" required type="email" />
            <label>
              <input name="subscribe" type="checkbox" />
              Yes, subscribe me to your newsletter.
            </label>
            <button type="submit">Subscribe</button>
          </form>
        </div>
        <div className="footer-info">
          <p>Breathe by Tammy Gallaway</p>
          <p>Mail: info@mysite.com</p>
          <p>Phone number: 123-456-7890</p>
        </div>
        <div className="footer-bottom">
          <p>
            © 2035 by Tammy Gallaway. Powered and secured by{' '}
            <a href="https://www.wix.com" style={{ color: '#FFFFFF' }}>
              EmoSong
            </a>
          </p>
        </div>
      </footer>
    );
  };
  

export default Footer;