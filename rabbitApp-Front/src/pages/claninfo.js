import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './css/infoclan.css';
import devav from './img/mainimg/derak.png'
const API_URL = 'https://rabbit-test.ru/';

function Main() {
  const [userData, setUserData] = useState(null);
  const [clanData, setClanData] = useState(null);
  const [topPlayers, setTopPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [clanId, setClanId] = useState(null); // Clan ID from profile
  const [queryId, setQueryId] = useState(null);
  const [profileData, setProfileData] = useState(null);
  const [farmn, setFarmn] = useState(1);
  const navigate = useNavigate();

  // Initialize Telegram WebApp
  useEffect(() => {
    const { WebApp } = window.Telegram;
    WebApp.BackButton.hide();
    WebApp.disableVerticalSwipes();
    WebApp.expand();
    
    const user = WebApp.initDataUnsafe?.user;
    const queryId = WebApp.initData;

    if (user) {
      setUserData({
        username: user.username,
        id: user.id,
      });
    }

    if (queryId) {
      setQueryId(queryId);
    }
  }, []);

  // Fetch profile and clan_id
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await axios.get(`${API_URL}/profile/${farmn}`, {
          headers: {
            'custom-header': queryId,
          },
        });

        const profile = response.data;
        setProfileData(profile);
        setClanId(profile.clan_id);
      } catch (error) {
        setError('Error loading profile');
      }
    };

    if (userData && queryId) {
      fetchProfileData();
    }
  }, [userData, queryId, farmn]);

  // Fetch clan data
  useEffect(() => {
    const fetchClanData = async () => {
      try {
        if (clanId) {
          const response = await axios.get(`${API_URL}/clan/${clanId}`);
          setClanData(response.data);
        }
      } catch (error) {
        setError('Error fetching clan data');
      }
    };

    const fetchTopPlayers = async () => {
      try {
        if (clanId) {
          const response = await axios.get(`${API_URL}/clan/members/${clanId}`);
          setTopPlayers(response.data);
        }
      } catch (error) {
        setError('Error fetching top players');
      }
    };

    if (clanId) {
      fetchClanData();
      fetchTopPlayers();
    }
  }, [clanId]);

  // Copy clan code function
  const copyClanCode = () => {
    const clanCode = clanData?.id || 'UNKNOWN';
    navigator.clipboard.writeText(clanCode);
    triggerHapticFeedback();
    alert('Clan code copied to clipboard!');
  };

  // Haptic feedback
  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred('medium');
  };

  // Invite to clan
// Invite to clan function
const inviteToClan = async () => {
  try {
    await axios.patch(`${API_URL}/clan/invite/`, null, {
      params: { id_clan: clanId },
      headers: { 'custom-header': queryId },
    });

    const inviteLink = `${API_URL}clan/invite/?id_clan=${clanId}`;
    navigator.clipboard.writeText(inviteLink); // Copy invite link to clipboard
    alert('Invitation link copied to clipboard!');
    triggerHapticFeedback();
  } catch (error) {
    setError('Error sending invite');
  }
};

// Leave clan function
const leaveClan = async () => {
  try {
    await axios.patch(`${API_URL}/clan/leave/`, null, {
      headers: { 'custom-header': queryId },
    });
    alert('You left the clan');
    triggerHapticFeedback();
  } catch (error) {
    if (clanData?.id_owner === userData?.id) {
      alert('You are the owner of the clan and cannot leave!');
    } else {
      setError('Error leaving clan');
    }
  }
};


  return (
    <div className="maininfoclan">
      <header>
        <div>
          <div className='headone'>
            <img src={profileData?.avatar || devav} alt="Avatar" className='avatar'/>
            <div className='wallet walletp'>
              <p className='clanname'>@{userData?.username || 'Username not available'}</p>
              <p className='clanname'>{clanData?.name || 'No clan'}</p>
              <p className='clanname' onClick={copyClanCode}>Clan ID: {clanData?.id || 'N/A'}</p>
            </div>
          </div>
        </div>
      </header>
      <p className='info t'>@{userData?.username || 'Username not available'}</p>
      <p className='info'>{clanData?.clan_balance || '0'} $CRT</p>
      <div className='inlebtn'>
        <button onClick={inviteToClan}>INVITE</button>
        <button onClick={leaveClan}>LEAVE</button>
      </div>
<h1 className='h1inf'>CLAN INFO:</h1>
<div className='claninf'>
  <span><p>ID</p><p>{clanData?.id || 'Unknown'}</p></span>
  <span><p>NAME</p><p>{clanData?.name || 'Unknown'}</p></span>
  <span><p>RANK</p><p>{clanData?.rank || 'Unknown'}</p></span>
  <span><p>IN TOP</p><p>{clanData?.in_top || 'Unknown'}</p></span>
  <span><p>BALANCE</p><p>{clanData?.clan_balance || '0'} $CRT</p></span>
  <span><p>COLLECTED</p><p>{clanData?.clan_collacted || '0'} $CRT</p></span>
  <span><p>MEMBERS</p><p>{clanData?.amount_members || '0'}</p></span>
  <span><p>OWNER ID</p><p>{clanData?.id_owner || 'Unknown'}</p></span>
</div>

      <h1 className='h1inf'>TOP PLAYERS:</h1>
      <div className='claninf'>
        {topPlayers.slice(0, 5).map((player, index) => (
          <span key={index}><p>{index + 1}.</p><p>@{player.nick_name}</p><p>{player.points} $CRT</p></span>
        ))}
      </div>
      <button className='watering leadboardclanbtn' onClick={triggerHapticFeedback}>CLAN LEADERBOARD</button>
      <footer>
        <div className='fotbtns'>
          <Link to="/" style={{textDecoration:"none"}}><button className='homeclan' onClick={triggerHapticFeedback}>HOME</button></Link>
        </div>
      </footer>  
    </div>
  );
}

export default Main;
