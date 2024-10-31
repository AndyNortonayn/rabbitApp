import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './css/createclan.css';
import creclanav from './img/creclan/rabclub.svg';

axios.defaults.baseURL = 'https://rabbit-test.ru/'; // Base URL for your API

function Main() {
  const [userData, setUserData] = useState(null);
  const [clanData, setClanData] = useState(null);
  const [clans, setClans] = useState([]);
  const [searchTerm, setSearchTerm] = useState(''); // State for search input
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const { WebApp } = window.Telegram;
    WebApp.BackButton.show();
    WebApp.BackButton.onClick(() => {
      navigate(-1);
    });
  
    const user = WebApp.initDataUnsafe?.user;
    const queryId = WebApp.initData;
    if (user) {
      setUserData({
        username: user.username,
        avatarUrl: user.photo_url,
        queryId: queryId
      });
    }
  
    const fetchClanData = async () => {
      try {
        // Fetch all clans
        const clansResponse = await axios.get('/clan', {
          headers: { 'custom-header': queryId }
        });
        setClans(clansResponse.data);
  
        // Fetch user profile
        const profileResponse = await axios.get('/profile/1', {
          headers: { 'custom-header': queryId }
        });
  
        const clanId = profileResponse.data.clan_id;
        if (clanId) {
          const clanResponse = await axios.get(`/clan/${clanId}`, {
            headers: { 'custom-header': queryId }
          });
          setClanData(clanResponse.data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
  
    fetchClanData();
  }, [navigate]);

  const joinClan = async (idClan) => {
    if (clanData) {
      alert(`You are already in the clan ${clanData.name}. You cannot join another clan!`);
    } else {
      try {
        const { queryId } = userData;
        await axios.patch('/clan/add_member/', null, {
          params: {
            id_clan: idClan
          },
          headers: {
            'custom-header': queryId
          }
        });
        setResponseMessage('You successfully joined the clan!');
        setClanData({ id: idClan });
        navigate("/claninfo");
      } catch (err) {
        setError('Failed to join the clan');
      }
    }
  };

  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred('medium');
  };

  // Filter clans by search term
  const filteredClans = clans.filter((clan) =>
    clan.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="main-creclan">
      <header>
        <div>
          <div className='headone'>
            <p className='h1tasks'>JOIN ONE</p>
          </div>
        </div>
      </header>
     
      {/* Search input */}
      <input
        className='finder'
        placeholder='Find clan by name'
        value={searchTerm} // Bind input value to state
        onChange={(e) => setSearchTerm(e.target.value)} // Update state on change
      />
     
      <div className='list-clan'>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className='lists'>
            {filteredClans.map((clan) => ( // Use filteredClans instead of clans
              <div key={clan.id} className='clan-item'>
                <p className='pp'>{clan.name}</p>
                <p className='ppp'>{clan.amount_members} members</p>
                <button onClick={() => joinClan(clan.id)}>Join</button>
              </div>
            ))}
            {responseMessage && <p>{responseMessage}</p>}
          </div>
        )}
      </div>

      <footer>
        <img src={creclanav} width={250} alt="Clan Avatar"/>
        <div className='fotbtns'>
          <Link to="/" style={{ textDecoration: "none" }}>
            <button className='homeclan' onClick={triggerHapticFeedback}>HOME</button>
          </Link>
        </div>
      </footer>
    </div>
  );
}

export default Main;
