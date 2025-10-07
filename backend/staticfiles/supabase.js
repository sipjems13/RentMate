// Supabase configuration and authentication functions
// You'll need to replace these with your actual Supabase project credentials

const SUPABASE_URL = 'https://rdzmlzrsvmewwizimgnb.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_rD3RjsKnJAtMOlGggsFr9g_rK9RitvU';

// Initialize Supabase client
let supabase = null;

// Initialize Supabase when the script loads
async function initSupabase() {
    if (typeof window !== 'undefined' && window.supabase) {
        supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        return true;
    }
    return false;
}

// Initialize on load
initSupabase();

export async function supabaseSignUp(payload) {
    try {
        if (!supabase) {
            const initialized = await initSupabase();
            if (!initialized) {
                throw new Error('Supabase client not available. Please ensure Supabase script is loaded.');
            }
        }

        const { email, password, firstName, lastName, role } = payload;
        
        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password,
            options: {
                data: {
                    first_name: firstName,
                    last_name: lastName,
                    role: role || 'tenant'
                }
            }
        });

        if (error) {
            throw new Error(error.message);
        }

        return data;
    } catch (error) {
        console.error('Supabase signup error:', error);
        throw error;
    }
}

export async function supabaseSignIn(email, password) {
    try {
        if (!supabase) {
            const initialized = await initSupabase();
            if (!initialized) {
                throw new Error('Supabase client not available. Please ensure Supabase script is loaded.');
            }
        }

        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });

        if (error) {
            throw new Error(error.message);
        }

        // Store the session token for future requests
        if (data.session) {
            localStorage.setItem('supabase_token', data.session.access_token);
        }

        return data;
    } catch (error) {
        console.error('Supabase signin error:', error);
        throw error;
    }
}

export async function supabaseSignOut() {
    try {
        if (!supabase) {
            const initialized = await initSupabase();
            if (!initialized) {
                throw new Error('Supabase client not available. Please ensure Supabase script is loaded.');
            }
        }

        const { error } = await supabase.auth.signOut();
        
        if (error) {
            throw new Error(error.message);
        }

        // Clear stored tokens
        localStorage.removeItem('supabase_token');
        localStorage.removeItem('rentmate_token');
        
        return true;
    } catch (error) {
        console.error('Supabase signout error:', error);
        throw error;
    }
}

export async function getCurrentUser() {
    try {
        if (!supabase) {
            const initialized = await initSupabase();
            if (!initialized) {
                return null;
            }
        }

        const { data: { user }, error } = await supabase.auth.getUser();
        
        if (error) {
            console.error('Error getting current user:', error);
            return null;
        }

        return user;
    } catch (error) {
        console.error('Error getting current user:', error);
        return null;
    }
}
